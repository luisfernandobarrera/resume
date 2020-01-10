## Personal CV Building System ##

I'm fed up with the format of my CV and I decided to move all data to a JSON File with the [resume.json format](https://jsonresume.org/).

I adapted one of the themes and modified it to my needs using SASS, Jinja2 and Frozen Flask to template and generate static pages. It will read a file with `.resume.json` extension in the root file.

The CSS is optimized for screen and print.

To install just execute:

```bash
pip install -r requirements.txt
```

To generate the static files

```python
python gen_static.py
```

To develop your cv
```bash
python -m flask run 
```

Inside the `templates` folder you will find the template and the SASS file.

### TODO ###

- A hook to update the `docs/` folder after each commit.
- Finish the format
- Generate the PDF in the same process.