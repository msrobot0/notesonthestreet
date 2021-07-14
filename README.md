::Notes On the Street

This turns a list of pdfs into images with the name of the pdf written at the top of the image

It is alpha

i have only tested in on osx 10.15

To run  on osx 
brew install poppler (https://formulae.brew.sh/formula/poppler)

fire up the command line and type

You can use venv (I do ) and do this in venv


python -r requirements.txt
python main.py python main.py source_dir dest_dir optional_max_pdfs

I suppose I could make a nice install script and chown things - maybe in the future


Thanks to Nitzan for the inspiration https://byed.it/ 