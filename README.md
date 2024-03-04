# BizCardX: Extracting Business Card Data with OCR #
### Description: ##
**The project aims to develop a Streamlit application utilizing easyOCR for extracting vital details from uploaded business card images. Users can upload images, and relevant information like company name, holder details, contact info, and location will be extracted and displayed in an intuitive GUI. Additionally, users can save extracted data along with the uploaded image into a database, facilitating efficient management of multiple entries. Combining image processing, OCR, GUI development, and database management, the project offers a user-friendly solution for organizing and storing business card information effectively.**

## Introduction: ##
    The project entails developing a streamlined business card information extraction application using Python, Streamlit, and easyOCR, integrated with a database management system such as SQLite or MySQL. With a user-friendly interface, the application facilitates effortless uploading of business card images, extraction of pertinent details, organized display, and seamless storage into a database, offering enhanced efficiency in managing business contacts.

### Libraries/Modules Required ###

- easyOCR: For performing Optical Character Recognition (OCR) on the uploaded business card images.
- mysql.coonector: To connect and interact with MySQL database for storing extracted information.
- streamlit: For building the graphical user interface (GUI) of the application and managing user interactions.
- streamlit_option_menu: A module for creating interactive option menus within Streamlit applications.
- pandas: Useful for data manipulation and organization, particularly when dealing with tabular data.
- cv2: OpenCV library for image processing tasks such as resizing, cropping, and enhancing image quality.
- os:  Provides functions for interacting with the operating system, facilitating tasks like file handling.
- re:  Regular expression module for pattern matching and text manipulation.

### Approach: ###

- *Package Installation:* Install Python, Streamlit, easyOCR, and a suitable database management system like SQLite or MySQL.
- *User Interface Design:* Develop a simple and intuitive Streamlit interface facilitating image upload and information extraction using widgets such as file uploaders and buttons.
