# Val.Es.Co. Conversation Processing

This repository contains tools and resources for processing and analyzing conversations following the **Val.Es.Co. model** (*Valencia, Español Coloquial*). The conversations are stored in **.eaf (ELAN Annotation Format)** files, adapted to our specific annotation system.  

⚠ **Note:** All scripts in this repository are designed to work exclusively with **.eaf files formatted according to the Val.Es.Co. model**. If your files do not follow this structure, modifications may be required.

## Features

- **Processing of annotated conversations** in .eaf format following our adapted Val.Es.Co. structure.
- **Conversion tools** to extract and structure data from ELAN files.
- **Analysis scripts** for conversation modeling.
- **Customization options** to adjust the workflow for different research needs.

## Installation

To use this project, you need to have **Python 3.x** installed. Clone the repository and install the required dependencies.

## File Structure
This repository contains the following scripts, all specifically designed to handle .eaf files formatted according to the Val.Es.Co. model:

dot_cleaner.py
Cleans and preprocesses .eaf files by replacing colons (:) in ANNOTATION_VALUE tags with <al/>. It ensures that annotations conform to the required standards and saves the cleaned version in a new file.

info_extractor.py
Extracts metadata and structural information from .eaf files using pympi.Elan. It lists available tiers and provides sample annotations to facilitate understanding of the transcription file's structure.

timeline.py
Generates timeline visualizations of conversations based on subact data stored in an Excel file. Uses pandas and matplotlib to plot conversation interventions, assigning distinct colors to different subact types for clear differentiation.

transcription_extractor.py
Converts conversations from Word documents in the old Val.Es.Co. format into a draft .eaf version. This script facilitates the migration of transcriptions to the ELAN annotation format, preserving conversational structure for further annotation and analysis.

## Contributing
We welcome contributions to improve the project. Feel free to:

## Submit issues for bugs or feature requests.
Fork the repository and open a pull request with your improvements.
License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or collaboration, feel free to reach out via GitHub Issues or email.

```bash
git clone https://github.com/Nikki21212121/Corpus-work.git
cd Corpus-work
pip install -r requirements.txt
