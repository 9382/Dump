### Funny python indentation ###
# Indentation must be consistent within its statement, but can vary when going into substatements
# e.g. 2 tabs into 2 spaces into 1 tab is legal as long as you're consistent about it within a statement
# (See the first else: for said case)

if True:
	print("A")
	if True:
	    print("B")
	    if True:
	    	print("C")
else:
		print("D")
		if True:
		  print("E")
		  if True:
		  	print("F")
