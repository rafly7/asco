#author : rafly dipoe.a
import argparse
import asyncio
import aiohttp
import sys
import time

#Scope variable
loop = asyncio.get_event_loop()
LG='\033[1;32m' #green
DT='\033[0m' # Default
R='\033[0;31m' #red

def _argument():
	parser = argparse.ArgumentParser(description="Cheking xss url",formatter_class=argparse.RawTextHelpFormatter)
	parser.add_argument("-u",metavar="URL",dest="url",help="url target")
	parser.add_argument("-o",metavar="OUTPUT",dest="output",help="output filename")
	parser.add_argument("-d",metavar="DICTIONARY",dest="dictionary",help="file dictionary (default payload.txt)",default="payload.txt")
	return parser

#Checking if url start with protocol https or http
def protocol(url):
	if url.startswith("https://") or url.startswith("http://"):
		return url
	else:
		if url.startswith("www"):
			return f"https://{url}"
		else:
			return f"http://{url}"

async def argument_req():
	global output
	arg = _argument().parse_args()
	if arg.output:
		output = arg.output
	if arg.url:
		#start time async requests
		ts = time.time()
		session = aiohttp.ClientSession()
		
		#gather url and payload with list in nested for async
		for f in asyncio.as_completed([session.get(f"{arg.url}/{i}") for i in open(arg.dictionary,"r").readlines()]):
			try:
				resp = await f
				if resp.status == 200:
					print(f"\r{LG}[+] May Vulnerable Xss {resp.status}{DT}",end="")
					f=open(output,"a+")
					f.write(f"\n{resp.url}")
				else:
					print(f"\r{R}[-] Not Vulnerable Xss {resp.status}{DT}",end="")
				#buffered screen response url
				sys.stdout.flush()
				await resp.release()
			except Exception:
				continue
		await session.close()
		print(f"\noutput : {output}\nFinished : {(time.time() - ts):.2f} seconds")

def main():
	loop = asyncio.get_event_loop()
	loop.run_until_complete(argument_req())
	loop.close()

def banner():
	print("""

 █████╗ ███████╗ ██████╗ ██████╗ 
██╔══██╗██╔════╝██╔════╝██╔═══██╗
███████║███████╗██║     ██║   ██║
██╔══██║╚════██║██║     ██║   ██║
██║  ██║███████║╚██████╗╚██████╔╝
╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═════╝ 
	""")

if __name__ == "__main__":
	banner()
	main()
	
	
