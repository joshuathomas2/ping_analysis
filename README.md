# pinganalysis.pyw

- Run pinganalysis.pyw
- Select file from listbox on the left to analyze
- Once selected, press the Analyze button

## Creating your own files
- To create your own file to analyze click the Open CMD button
- ping [address] -t > [filename.txt]
- Let it run for as long as you would like. You can keep it running and analyze it at the same time.
- Once you are done with it, you can press CTRL + C or simply exit the CMD prompt window.
- Click the Refresh List button
- Select your text file from the list and click the Analyze button

## settings.json
- Set your own values in settings.json
- pinganalysis.pyw will remember if you use Light Theme or Dark Theme the next time you run the program

## TODO

- Implement Checkbutton that when checked automatically runs self.analyze()
- Add graphs from matplotlib