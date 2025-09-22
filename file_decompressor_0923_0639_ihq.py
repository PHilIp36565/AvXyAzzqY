# 代码生成时间: 2025-09-23 06:39:32
import os
import zipfile
import tarfile
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application

"""
A Tornado web application that provides a simple file decompression service.
"""

class DecompressHandler(RequestHandler):
    """
    Handles the HTTP requests for decompressing files.
    """
    def post(self):
        # Get the uploaded file from the request
        file = self.request.files['file'][0]
        filename = file['filename']
        file_data = file['body']

        try:
            # Check the file extension to determine the decompression method
            if filename.endswith('.zip'):
                self.decompress_zip(file_data)
            elif filename.endswith(('.tar', '.tar.gz', '.tgz')):
                self.decompress_tar(file_data)
            else:
                self.write({'error': 'Unsupported file format'})
                return

            # Respond with success message
            self.write({'message': 'File decompressed successfully'})
        except Exception as e:
            # Handle any errors that occur during decompression
            self.write({'error': str(e)})

    def decompress_zip(self, file_data):
        """
        Decompress a zip file.
        """
        with zipfile.ZipFile(file_data, 'r') as zip_ref:
            zip_ref.extractall(self.get_temp_dir())

    def decompress_tar(self, file_data):
        """
        Decompress a tar file.
        """
        with tarfile.open(fileobj=file_data, mode='r') as tar_ref:
            tar_ref.extractall(self.get_temp_dir())

    def get_temp_dir(self):
        """
        Returns a temporary directory path for extracting files.
        """
        # In a real-world application, consider using a more robust temporary file management solution
        return os.path.join(os.getcwd(), 'temp')

def make_app():
    """
    Creates a Tornado application with the decompression handler.
    """
    return Application([
        (r"/decompress", DecompressHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Server is running on http://localhost:8888")
    IOLoop.current().start()
