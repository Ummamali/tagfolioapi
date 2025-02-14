# Tagfolio - NLP Based Multimedia Manager 🚀 📷
### REST API For Tagfolio

TagFolio is a revolutionary platform designed to address the growing complexity and importance of multimedia content management and analysis in today's digital landscape. 

With its comprehensive suite of modules, TagFolio offers users a seamless and intuitive experience for tagging, organizing, and analyzing multimedia data across various domains. 

From user management to image and video tagging, multimedia organization, text detection, social media analysis, and advanced natural language processing capabilities, TagFolio provides a holistic solution to streamline the entire workflow of handling multimedia content. 

Web interface repository: https://github.com/Ummamali/webtagfolio

## Key Features  

- **Image Tagging** – AI-powered object and person recognition for efficient media organization.  

- **Management Portal** – Edit, delete, and organize images & videos effortlessly.  

- **Video Tagging** – Smart recognition and tagging of video content.  

- **Media Enhancement** – Apply filters, edit images, and enhance media quality.  

- **Similarity Checker** – Detect and compare similar images with AI precision.  

- **Text Detection** – Extract and analyze text from images and videos.  

- **Social Media Analyzer** – Gain insights from multimedia content across social platforms.  

- **NLP-Based Chatting Agent** – AI-driven chatbot for seamless user interaction.  

- **Emotional Analysis** – Understand sentiment and emotions in media content.


## Installation

### Prerequisites

Ensure you have the following installed:

- [Python 3] (https://www.python.org/)  
- [TensorFlow] (https://www.tensorflow.org/)  
- [Flask] (https://flask.palletsprojects.com/)  
- [OpenCV] (https://opencv.org/)  

### Setup

1. Clone the repository:  
   ```sh
   git clone https://github.com/Ummamali/tagfolioapi.git
   cd tagfolioApi

### How to run this backend server

#### Step 0: Clone and install the dependencies

This project is managed by pipenv

- Install pipenv
  > pip install pipenv
- Install Dependencies
  > pipenv install

#### Step 1: Run the database

Go to the tagfoliops repository and run the docker-compose file in database folder

#### Step 2: Add dummy data in the database

In the root of this application there is a migrations.py file. Run it as

python migrations.py

## Usage

### 1. Dashboard
The **Dashboard** provides an overview of the application, featuring:
- **Side Navigation**: Quick access to different sections.
- **Popular Buckets**: Displays frequently accessed storage buckets.

### 2. Bucket Explorer
The **Bucket Explorer** allows users to:
- Browse and navigate through stored buckets (folders).
- View details and metadata of each bucket.
- Perform operations such as renaming or deleting buckets.

### 3. Chat
The **Chat Module** functions like a messaging interface (similar to WhatsApp):
- **Real-time messaging**: Users can send and receive messages.
- **Threaded conversations**: Messages are grouped within specific topics.

### 4. Image Data Viewer
The **Image Data Viewer** is similar to Unsplash, offering:
- A grid layout displaying images.
- Detailed view with metadata when an image is clicked.
- Search and filter options to find specific images.

### 5. Image Object Tagging
The **Image Tagging Tool** provides:
- **Drag-and-drop functionality**: Users can draw bounding boxes around objects.
- **AI-assisted tagging**: Suggests object labels based on AI detection.
- **Manual adjustments**: Users can rename or adjust object tags.

### 6. Upload Image
The **Image Upload Module** allows users to:
- Upload images from their device.
- Process images for AI-based tagging.
- Review and confirm object tags before saving.

### 7. Upload Video
The **Video Upload Module** supports:
- Uploading video files.
- AI-based video analysis for tagging.
- Managing and storing tagged video content.


## Frontend Technologies

The frontend of this application is built using modern web technologies to ensure a fast, responsive, and scalable user experience.

- **Next.js** – For server-side rendering and optimized React applications.  
- **React.js** – Component-based UI development.  
- **JavaScript (JS)** – Core scripting language for interactivity.  
- **HTML & CSS** – Structure and styling of web pages.  
- **TailwindCSS** – Utility-first styling for faster and more maintainable designs.


## License

This project is licensed under the **MIT License**.  

### Step 3: Run the server

> pipenv shell
> python api.py
