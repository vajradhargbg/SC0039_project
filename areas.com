>for iz in range(4):
$ clipmodel -z %iz,%iz flagellum.mod temp.mod
$ imodinfo temp.mod
