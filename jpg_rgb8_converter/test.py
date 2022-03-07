import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String

from PIL import Image as pil_image
from io import BytesIO
import base64

'''
Designed :
    node : 
        jpg_rgb8_converter_node
    pub :
        publisher:
            topic : /jpg_uri
    sub :
        subscription :
            topic : /rgb_cam/image_raw
'''


class jpg_rgb8_converter_node(Node):

    def __init__(self):        
        
        # node
        super().__init__('jpg_rgb8_converter_node')

        # pub
        self.publisher = self.create_publisher(
            String,
            'jpg_uri',
            10
        )
        
        # sub
        self.subscription = self.create_subscription(
          Image,
          '/rgb_cam/image_raw',
          self.listener_callback,
          10
        )

        # prevent unused variable warning
        self.publisher
        self.subscription


    def listener_callback(self, rgb8_data):
        
        # convert to jpg
        img = pil_image.frombytes('RGB', (rgb8_data.width, rgb8_data.height), rgb8_data.data.tobytes())

        # jpg get uri
        uri = String()
        uri.data = self.pil_to_datauri(img)

        # publish uri
        self.publisher.publish(uri)


    @staticmethod
    def pil_to_datauri(img):
        # converts PIL image to datauri
        data = BytesIO()
        img.save(data, "JPEG")
        data64 = base64.b64encode(data.getvalue())
        return u'data:img/jpeg;base64,'+data64.decode('utf-8')


def main(args=None):
    rclpy.init(args=args)

    jrcn = jpg_rgb8_converter_node()

    rclpy.spin(jrcn)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    jrcn.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()