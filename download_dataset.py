from roboflow import Roboflow
rf = Roboflow(api_key="rzg7mVOjycENkePsBAXc")
project = rf.workspace("sriraams17-gmail-com").project("office-yt3rl-hawby")
version = project.version(1)
dataset = version.download("yolov8")
                