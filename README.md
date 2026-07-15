# snaplm

## Why "SnapLM"?

**SnapLM** stands for **Snapdragon Language Models**.

SnapLM is an open-source tool for detecting hardware capabilities, benchmarking local inference, and helping users run language models efficiently—starting with Snapdragon-powered Windows devices.

Its goals are to:

- detect hardware capabilities
- benchmark local inference performance
- recommend appropriate models and execution backends
- make local AI easier to understand, especially on Windows on ARM

The project currently targets Qualcomm Snapdragon Windows devices but is designed to expand to other platforms over time.

## The real struggle 

This project is the result of my fascination with the way AI is developing and growing. As a proud self-learner, I began learning about local LLMs from random Reddit threads and YouTube video links, especially with my rather stingy obsession with getting free stuff, AI tokens being no exception. What started as a two-day adventure of trying to run models on my laptop, an oscillating sine curve ranging from being excited about discovering new models to despondent about the rather hefty storage volume and almost-infinite download time, combined with my frustration at Docker being rather stubborn about doing everything but working right, eventually led to various UIs for these local LLMs successfully taking up residence on my PC, except the models themselves, when prompted to run, were rather... unresponsive.

Naturally, as I never really had any interest in hardware in school, and always skimmed the electronics sections of my Physics syllabus, I had no idea why these models shouldn't run, when I clearly had the storage space to do so. I mean, I had way more than just 64 GB on my computer, the models were only like 20GB, and my ChatGPT had already assured me those models could run? Until I realized the difference between RAM and my regular storage. I was naturally severely disappointed to learn the limitations of storage memory.

Well, no problem. I'd just download smaller models. I wasn't very accustomed to the issues of my laptop beyond some differences in architecture that prevented me from, say, running Fortnite or any android simulator (thankfully Fortnite updated its architecture so running the game was no longer an issue at least, though I can't say the same for other apps) but I had learned to live with those issues. But why on earth if the RAM was now greater than the size of those models present on my computer, would those models still not proceed past the loading button? It made no sense.

That's when I learned about the rather unique issues with the laptop I had inherited. Namely, that the processor itself is special, for lack of other vocabulary, due to having an integrated RAM. What does that mean? Well, a lot of terminology, an Adreno GPU, a Hexagon NPU, and a lot more jargon which sound very futuristic but which I couldn't care less about if I had to make them from scratch. But what I learned, to summarize in 30 words or less, was that a lot of Ollama-based LLM backends don't fully utilize the acceleration hardware provided by Windows on ARM devices, so they... execute on the CPU instead. In my head, that meant the models were constantly bouncing work back and forth through main memory, and that, combined with CPUs just being slow as hell when it comes to these language models, meant that the entire process of answering a "hi!" was taking longer than it took me to finish a novel. Which was very frustrating. Of course, that's just one hypothesis for why it's so slow, it could still be others. But after much research, considering I did still want those open weight models on my laptop, make be damned, I came to the conclusion I must create my own tool for it. And this is going to be the result. Hopefully it analyzes the right stuff and tells me the core issue. And then, with luck, I can fix the backend so those models do run. One can only hope.

And if it is indeed successful, it will be the first time I am truly interested in hardware, probably because I get to actually work on it as opposed to memorizing facts in my brain for an exam where I would never use said facts again. In this case, it *should* hopefully be able to figure out which parts of the memory are available from my RAM, and accordingly ensure the LLMs run where they're supposed to, in a way that is fast rather than slower than a rusty old cycle stuck in the middle of quicksand. No idea why that mental image came to my mind but let's roll.

Of course, the more I thought about it, the more greedy my scope has become. Because I realized that, just as I struggled with understanding why my LLMs weren't cooperating with my own system, of course other people wouldn't be able to understand why it didn't work for them. Whether it's why inference is so slow, which hardware is utilized, whether acceleration is available or which model is appropriate for their system, existing tools kind of assume you already know this info. This tool should help you piece it together without needing another piece of AI to tell you how to run the first one. God knows we have enough AI to deal with already.

In short, the long term goal of SnapLM would hopefully be to become a companion to local AI. I see the future of AI not with a billion different data centres (then again I'm not very good at reading into the future so take whatever I say with a bag of salt, a grain may be too little) but rather local AI open weight models installed on our machines. Hopefully I haven't jinxed what is currently free of course, where people automatically start trying to monetize anything that sounds like a future investment. But rather than simply launching a model, SnapLM will hopefully be able to detect and analyze system hardware, identify CPU, GPU and NPU acceleration, benchmark local inference performance, recommend models that balance speed, memory usage and quality, suggest the most appropriate inference backend for detected hardware and provide a consistent interface across different hardware platforms and operating systems. 

Of course, it is currently suited to my laptop, a Qualcomm Snapdragon Windows device, but the aim is to get that support out to other systems like the x86 Windows, Linux, MacOS, Apple Silicon, NVIDIA CUDA, AMD ROCm, Intel accelerators and other hardware.

At the end of the day, this may be a tool I'm using to make my life easier, but it's also a learning project. I'm using it to understand how others perform software engineering, Python packaging, hardware detection and all kinds of other goodies surrounding local language model inference, and if it's of some use to anybody, then I'm already more than satisfied. It's just a way to bridge the gap a little closer between the resources at our disposal and the efficiency we'd like to reach after all. Nothing crazy.

> [!WARNING]
> If you've made it this far, thank you! One small disclaimer before you go: a lot of the technical explanations above are *very* intentionally oversimplified (if it wasn't obvious, heh) because this README is meant to tell the story of how I ended up building SnapLM, not teach computer architecture. If you're here to learn how unified memory, inference backends, GPUs or NPUs actually work, I'd strongly recommend checking out official documentation or a good ol' textbook. This repository is my learning journey, not the final authority.