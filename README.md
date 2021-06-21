# HumanLoop-Debugger

A web-app based debugger for HumanLoop

## Discussion

I would be hard-pressed to call this a debugger tool. It ended up being more of a visualisation dashboard. Partly because of the time spent on finangling Plotly's Dash to work as I wanted it to. 

I think if time permitted and the prediction API was working there might have been some interesting stuff that could have been done, as well some low hanging fruit like classification confusion matrices etc. 

I also believe the language model used is BERT based, so something like t-SNE clustering on the sentence embeddings from the BERT model might have made for one very interesting visualisation. (Allowing one to identify clusters of data points where classification intent was different but the latent representations were strongly overlapped or have high cosine similarity). A quick google tells me there is a way of computing fixed length sentence embeddings from BERT (and adjacent) models. [Link](https://arxiv.org/pdf/1908.10084.pdf)

**N.b. this web app is based off a Plotly Dash and the CookieCutter template SlapDash. The following instructions are taken from CC SlapDash, though simplified, and should allow you to install and use the web app relatively easily.**

### Installation

After cloning/downloading the repository, simply install HumanLoop-Debugger as a package into your target virtual environment:

I.e. something like: 

    $ pip install ./hl_debugger 

### Running The App

### Run App 

After having installed the app via pip to your virtual env you should have the following command added to your path while the venv is active:

    $ run-humanloop_debugger-dev

And now the web app should be running on the local server named in the output. 

### Screenshots

![](debugger_gif.gif)

![](screenshot_1.png)

![](screenshot_2.png)
