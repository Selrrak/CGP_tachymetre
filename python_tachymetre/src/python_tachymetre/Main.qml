import QtQuick
import QtQuick.Controls

ApplicationWindow {
    visible: true
    width: 600
    height: 400

    title: "Tachymètre"

    Column {
        anchors.centerIn: parent
        spacing: 20

        Text {
            text: tachymeter.rpm.toFixed(2) + " RPM"
            font.pixelSize: 48
        }

        Text {
            text: tachymeter.rps.toFixed(2) + " RPS"
            font.pixelSize: 24
        }

        Text {
            text: tachymeter.angular_velocity.toFixed(2) + " rad/s"
            font.pixelSize: 24
        }

        Text {
            text: tachymeter.centripetal_accel.toFixed(2) + " m/s²"
            font.pixelSize: 24
        }

        Text {
            text: tachymeter.centripetal_g.toFixed(2) + " G"
            font.pixelSize: 24
        }
    }
}

