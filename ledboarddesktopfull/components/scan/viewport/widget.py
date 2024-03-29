from PySide6.QtCore import QTimer, Signal
from PySide6.QtGui import QPen, QColor
from PySide6.QtWidgets import QWidget, QHBoxLayout, QGraphicsScene, QGraphicsRectItem, QGraphicsEllipseItem

from ledboardclientfull import DetectionPoint, scan_api

from ledboarddesktopfull.components.scan.viewport.detection_point_graphics_item import DetectionPointGraphicsItem
from ledboarddesktopfull.components.scan.viewport.interactors.navigator import Navigator
from ledboarddesktopfull.components.scan.viewport.interactors.mask_drawer import MaskDrawer
from ledboarddesktopfull.components.scan.viewport.interactors.detection_point_selector import DetectionPointSelector
from ledboarddesktopfull.components.scan.viewport.tools import ScanViewportTools
from ledboarddesktopfull.core.ui_components import UiComponents
from ledboarddesktopfull.python_extensions.graphics_view import GraphicsView
from ledboarddesktopfull.python_extensions.graphics_image_plane import GraphicsImagePlane


class ScanViewport(QWidget):
    viewportUpdated = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self._detection_points_items: dict[int, DetectionPointGraphicsItem] = dict()

        #
        # Widgets
        self.view = GraphicsView()
        self.scene = QGraphicsScene()

        self.image_plane = GraphicsImagePlane()

        self.horizontal_line = QGraphicsRectItem()
        self.horizontal_line.setPen(QPen(QColor(255, 255, 0)))

        self.detection_marker = QGraphicsEllipseItem()
        self.detection_marker.setRect(-5, -5, 10, 10)
        self.detection_marker.setPen(QPen(QColor(255, 0, 0)))

        self.scene.addItem(self.image_plane)
        self.scene.addItem(self.horizontal_line)
        self.scene.addItem(self.detection_marker)
        self.view.setScene(self.scene)

        self.tools = ScanViewportTools()

        #
        # Layout
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.tools)
        layout.addWidget(self.view, 100)

        #
        # Interactors
        self.viewport_navigator = Navigator(self.view, self.image_plane)
        self.viewport_mask_drawer = MaskDrawer(self.view)
        self.viewport_detection_point_selector = DetectionPointSelector(self.view)

        self.view.interactors.append(self.viewport_navigator)
        self.view.interactors.append(self.viewport_mask_drawer)
        self.view.interactors.append(self.viewport_detection_point_selector)

        self.image_plane.set_on_size_change_callbacks([
            self.viewport_navigator.fit,
            self._update_horizontal_line
        ])

        #
        # Signals
        self.tools.fitClicked.connect(self.viewport_navigator.fit)
        self.tools.maskEditingChanged.connect(self._mask_editing_changed)
        self.tools.maskResetClicked.connect(self._mask_reset)
        self.tools.maskToggleVisible.connect(self._mask_toggle_visible)
        self.tools.saveScanEditsClicked.connect(self._save_scan_edits)
        self.tools.assignSegmentIndex.connect(self._assign_segment_index)

        #
        # Timers
        self._viewport_timer = QTimer(self)
        self._viewport_timer.timeout.connect(self._update_viewport)

    def start_viewport_update_timer(self):
        self._viewport_timer.start(int(1000 / UiComponents().configuration.scan_viewport_framerate))

    def stop_viewport_update_timer(self):
        self._viewport_timer.stop()

    def _update_viewport(self):
        self.image_plane.setPixmap(scan_api.viewport_pixmap())
        self._make_scan_result_items()
        x, y, v = scan_api.get_detection_coordinates()
        self.detection_marker.setPos(x, y)
        self.viewportUpdated.emit()

    def _make_scan_result_items(self):
        scan_result = scan_api.get_scan_result()
        if scan_result is None:
            return

        for detection_point in scan_result.detected_points.values():
            if detection_point.led_number not in self._detection_points_items:
                new = DetectionPointGraphicsItem(detection_point)
                new.setPos(detection_point.x, detection_point.y)
                self._detection_points_items[detection_point.led_number] = new
                self.scene.addItem(new)

    def _mask_editing_changed(self, is_active):
        self.viewport_mask_drawer.is_active = is_active
        if not is_active:
            scan_api.set_mask(self.viewport_mask_drawer.mask)

    def _mask_reset(self):
        self.viewport_mask_drawer.reset()
        scan_api.reset_mask()

    def _mask_toggle_visible(self, is_visible):
        self.viewport_mask_drawer.mask_item.setVisible(is_visible)

    def load_from_client(self):
        self.viewport_mask_drawer.set_mask(scan_api.get_mask())  # FIXME: create ViewportMaskDrawer.load_from_client() ?

    def clear_detection_points(self):
        for item in self._detection_points_items.values():
            self.scene.removeItem(item)
        self._detection_points_items = dict()

    def _update_horizontal_line(self):  # FIXME: do better
        self.horizontal_line.setRect(
            0, self.image_plane.pixmap().height() / 2,
            self.image_plane.pixmap().width(), 0
        )

    def _save_scan_edits(self):
        result = scan_api.get_scan_result()
        for led_number, detection_point_item in self._detection_points_items.items():
            updated_detection_point = DetectionPoint(
                led_number=led_number,
                x=int(detection_point_item.x()),
                y=int(detection_point_item.y()),
                assigned_segment_number=detection_point_item.detection_point.assigned_segment_number
            )
            result.detected_points[led_number] = updated_detection_point
        scan_api.set_scan_result(result)

    def _assign_segment_index(self, index):
        for led_number, detection_point_item in self._detection_points_items.items():
            if not detection_point_item.isSelected():
                continue

            detection_point_item.detection_point.assigned_segment_number = index
            detection_point_item.update()
