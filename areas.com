>for iz in range(100):
$ clipmodel -z %iz,%iz model_file_here.mod temp.mod
$ imodinfo temp.mod