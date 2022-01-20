# Audiobook

Install flask app - pip install flask (or) pip3 install flask

Need to install tensorflow version 2.4.1 for the autoencoder model to run

run python app.py 

* Our proposed system of audiobook can be used for any printed material including books (school textbooks, storybooks), research papers, newspapers, documents (a 
single sheet of text or multiple pages which can also be dirty) wherein users have to just upload the printed information and enjoy listening to the content. Autoencoders are used to denoise the dirty documents.

* This is followed by OCR with PyTesseract.

* So far, the OCR methods do not have any post-correction methods. We have included an automatic spell check feature that detects spelling errors and corrects them according to the dictionary.

*  An E2E application in Flask is developed

