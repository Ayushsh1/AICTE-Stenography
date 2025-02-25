from PIL import Image
import numpy as np
import hashlib
import os

def encrypt(data, password):
    # Create a repeatable key from the password
    key = hashlib.sha256(password.encode()).digest()
    key_length = len(key)
    encrypted = bytearray()
    
    # XOR each byte of data with the corresponding byte from the key
    for i, byte in enumerate(data):
        encrypted.append(byte ^ key[i % key_length])
    return encrypted

def decrypt(data, password):
    return encrypt(data, password)  # XOR is reversible

def is_valid_image(image_path):
    valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.gif'}
    return os.path.splitext(image_path)[1].lower() in valid_extensions

def is_valid_image_size(image_path, max_size_mb=5):
    """Check if image size is within limit (5MB)"""
    file_size = os.path.getsize(image_path) / (1024 * 1024)  # Convert to MB
    return file_size <= max_size_mb

def encode_image(image_path, message, password, output_path):
    try:
        # Read and validate image
        with Image.open(image_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            data = np.array(img, dtype=np.uint8)

        # Prepare message with terminator
        message_bytes = message.encode('utf-8') + b'\x00'
        encrypted = encrypt(message_bytes, password)
        
        # Convert message length to 32-bit binary
        msg_len = len(encrypted)
        len_bits = format(msg_len, '032b')
        
        # Convert encrypted message to bits
        msg_bits = ''.join(format(byte, '08b') for byte in encrypted)
        
        # Total bits needed
        total_bits = len(len_bits) + len(msg_bits)
        if total_bits > data.size:
            raise ValueError("Message too large for image")

        # Embed length and message
        flat_data = data.flatten()
        
        # Embed length first (32 bits)
        for i, bit in enumerate(len_bits):
            flat_data[i] = (flat_data[i] & 0xFE) | int(bit)
            
        # Embed message bits
        for i, bit in enumerate(msg_bits):
            flat_data[i + 32] = (flat_data[i + 32] & 0xFE) | int(bit)

        # Save modified image
        modified = flat_data.reshape(data.shape)
        result = Image.fromarray(modified)
        result.save(output_path, 'PNG', optimize=False)
        return True

    except Exception as e:
        print(f"Encoding error: {e}")
        return False

def decode_image(image_path, password):
    try:
        if not is_valid_image(image_path):
            raise ValueError("Unsupported image format. Please use .jpg, .jpeg, .png, .bmp, or .gif")

        # Read image
        with Image.open(image_path) as img:
            if img.mode != 'RGB':
                img = img.convert('RGB')
            data = np.array(img)

        # Extract bits
        flat_data = data.flatten()
        
        # Get length (first 32 bits)
        len_bits = ''.join(str(byte & 1) for byte in flat_data[:32])
        msg_len = int(len_bits, 2)
        
        if msg_len <= 0 or msg_len > (len(flat_data) - 32) // 8:
            raise ValueError("Invalid message length")

        # Extract message bits
        msg_bits = ''.join(str(byte & 1) for byte in flat_data[32:32 + msg_len * 8])
        
        # Convert bits to bytes
        msg_bytes = bytearray()
        for i in range(0, len(msg_bits), 8):
            byte = msg_bits[i:i+8]
            msg_bytes.append(int(byte, 2))

        # Decrypt and decode
        decrypted = decrypt(msg_bytes, password)
        message = decrypted.split(b'\x00')[0].decode('utf-8')
        
        if not message:
            raise ValueError("No message found or incorrect password")
            
        return message

    except Exception as e:
        print(f"Decoding error: {e}")
        return None

if __name__ == "__main__":
    print("=== Steganography Tool ===")
    
    while True:
        choice = input("\n1. Encode\n2. Decode\n3. Exit\nChoice: ")
        
        if choice == '1':
            image_path = input("Input image path: ")
            message = input("Message to hide: ")
            password = input("Password: ")
            output_path = input("Output image path: ")
            
            if encode_image(image_path, message, password, output_path):
                print("Message encoded successfully!")
                
        elif choice == '2':
            image_path = input("Image path: ")
            password = input("Password: ")
            
            message = decode_image(image_path, password)
            if message:
                print(f"Decoded message: {message}")
                
        elif choice == '3':
            break
