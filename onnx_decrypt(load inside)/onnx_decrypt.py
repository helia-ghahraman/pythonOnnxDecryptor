from cryptography.fernet import Fernet
import onnxruntime
import onnx
import io

class DecryptAndLoadModel:

    def __init__(self, secret_key):
        self.secret_key = secret_key

    def decrypt_file(self, file_path):
        with open(file_path, 'rb') as file:
            encrypted_data = file.read()

        fernet = Fernet(self.secret_key)
        decrypted_data = fernet.decrypt(encrypted_data)

        return decrypted_data

    def load_model(self, decrypted_data):

        model = onnx.load(io.BytesIO(decrypted_data))

        return model

    def load_model_with_inference(self, decrypted_data):

        model = onnx.load_model_from_string(decrypted_data)

        # Print a human readable representation of the graph to test if the decryption worked
        # graph_str = onnx.helper.printable_graph(model.graph)
        # print(graph_str)

        session_options = onnxruntime.SessionOptions()

        session = onnxruntime.InferenceSession(model.SerializeToString(), session_options=session_options)

        return session

if __name__ == "__main__":

    secret_key = b'KCilyK8Fk9wHiuEc5PmbZbbcR-ue3VSsqFaoKZRcdvA='

    decryptor = DecryptAndLoadModel(secret_key)

    file_to_decrypt = 'onnx_encrypted_data.bin'

    decrypted_data = decryptor.decrypt_file(file_to_decrypt)

    model = decryptor.load_model(decrypted_data)
    session = decryptor.load_model_with_inference(decrypted_data)

    # onnx.checker.check_model(model)
    # Print a human readable representation of the graph to test if the decryption worked
    # print(onnx.helper.printable_graph(model.graph))
