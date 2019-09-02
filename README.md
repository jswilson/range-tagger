# range-tagger
Open source application to help manually label video datasets for use in machine learning

range-tagger is a Qt-based desktop application designed to help you quickly label sections of long videos manually.  It is designed to help you assign every frame in your video with a label so you can then use the data to train machine learning algorithms.

You can learn more about the motivation and design of range-tagger [here](https://www.jswilson.co/posts/posts/release-of-range-tagger/)

## Use case
When developing machine learning models, having properly labelled data for tranining is very important.  Let's suppose you want to build a machine learning model to automatically classify parts of a television broadcast into two classes: "commercial" or "part of the real show."  Your first step is going to be collecting a large amount of video data, but then you will need to manually label a portion of it for model training purposes.  range-tagger would let you quickly and accurately label segments of your videos as "commercials" or "show."  You would produce a CSV that looks something like this:

| Start Frame | End Frame | Label |
| ----- | ----------- |----------- |
| 0 | 1205 | commercial
| 1206 | 7660 | show
| 7661 | 9122 | commercial
| 9123 | 14565 | show
| ... | ... | ...

which you could then use to associate with frames that you feed into your model.

range-tagger does not handle "object detection" use cases; you can use a tool like [VoTT](https://github.com/microsoft/VoTT) to handle object detection.  range-tagger took inspiration from VoTT for its design, but ultimately handles a different use case.

## Getting Started
You can find the latest binary release [here](https://github.com/jswilson/range-tagger/releases), and you can find a demo video [here](https://youtu.be/sZvp8YXCoto).  Right now, range-tagger is only available on OSX; this is due to a single dependency.  If you would like to use range-tagger on Windows or Linux, just post an issue and I can help create a build for your platform.

### Keyboard shortcuts
range-tagger uses keyboard shortcuts to help make your life manually labelling videos much simpler.  The shortcuts are fairly quick to learn and will help you multiply your labelling productivity:

| Shortcut | Purpose |
| ----- | ----------- |
| ⇧⌘C | Create a new segment at the current frame
| ⇧⌘E | End the selected segment at the current frame
| ⌘Z | Undo
| ⇧⌘Z | Redo
| ⌘1 | Label current segment with the first tag
| ⌘2 | Label current segment with the second tag
| ⌘3 | Label current segment with the third tag
| ⌘4 | Label current segment with the fourth tag
| a | Move backward 100 times the base number of frames
| s | Move backward 10 times the base number of frames
| d | Move backward 1 times the base number of frames
| f | Move backward a single frame
| j | Move forward a single frame
| k | Move forward 1 times the base number of frames
| l | Move forward 10 times the base number of frames
| ; | Move forward 10 times the base number of frames

And these shortcuts are shown extensively in the demo video [here](https://youtu.be/sZvp8YXCoto).
