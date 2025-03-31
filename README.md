
# PDFEXTRACTOR

PDFEXTRACTOR is a powerful tool designed to extract text, images, and metadata from PDF documents efficiently. It simplifies document processing workflows and provides a seamless way to extract and analyze PDF content.

## Features
- Extract text from PDFs with high accuracy.
- Retrieve images embedded within PDFs.
- Extract metadata such as author, title, and creation date.
- Support for multiple PDF file handling.
- Simple command-line usage.

## Installation

### Prerequisites
Ensure you have the following installed on your system:
- Python 3.8 or later
- Git
- pip (Python package manager)

### Steps
1. Clone the repository:
   ```sh
   git clone https://huggingface.co/spaces/krishanmittal018/PDFEXTRACTOR
   cd PDFEXTRACTOR
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Verify installation:
   ```sh
   python app.py --help
   ```

## Usage
Run the script to extract text from a PDF:
```sh
python app.py --input example.pdf --output extracted_text.txt
```

Run on stramlit:
```sh
streamlit run app.py
```

Display metadata:
```sh
python app.py --input example.pdf --show-metadata
```

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`feature-branch`).
3. Commit your changes.
4. Push to your fork and submit a pull request.

## License
This project is licensed under the MIT License.

## Contact
For any inquiries, feel free to reach out:
- **Author:** Krishan Mittal
- **Email:** krishanmittal798@gmail.com
- **Hugging Face Space:** [PDFEXTRACTOR](https://huggingface.co/spaces/krishanmittal018/PDFEXTRACTOR)




