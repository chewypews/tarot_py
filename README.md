# How to use this...
1. Clone this repo.
2. Open terminal.
3. Activate a conda environment. 
4. Navigate to the directory of the repo (tarot_py). 
5. Open google chrome.
6. Run `python tarot.py -s {spread_type}` where `{spread_type}` is either *"one", "three", "bridge", or "celtic"*. 
7. Additional, optional arguments include:
    - `-q {question}` where `{question}` is a string that becomes part of the seed to inform the card-selection randomizer. 
    - `-f {filepath}` where `{filepath}` is the path to a .txt file that includes a list of cards. This argument is used if the user wishes to transcribe a spread that was drawn elsewhere. 
      - If using `{filepath}`, the following conditions must be met:
        - The number of cards in the .txt file must match the number of cards required in the spread. 
        - Each card must appear on its own line (with no extra spaces at the end or beginning of the line). 
        - Each card must be named exactly the same as the .png file in the cards/ folder -- e.g. the Fool is "majors_0."
        - Each card must be preceded with a + or - (+ indicates upright, and - indicates reversed).
      - See `example_filepath_for_celtic_transcription.txt` for an example of how to structure this file. 
8. Open the html, then print -> save as PDF :)

Examples of use:
  - `python tarot.py -s three` = "draw a three card spread"
  - `python tarot.py -s one -q "what is goin on?"` = "draw a one-card spread, and use the text after -q as part of the seed for the randomizer."
  - `python tarot.py -s celtic -f ~/tarot_py/example_filepath_for_celtic_transcription.txt` = "create a celtic cross spread using the cards listed in `example_filepath_for_celtic_transcription` to populate the reading. 


