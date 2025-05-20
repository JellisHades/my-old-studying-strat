import os
import sys
import shutil
from os import path
from importlib.machinery import SourceFileLoader
import docx
import time
import threading

import docx.enum
import docx.enum.text

FontName = "Arial"
FontSize = 11
BigFontSize = 15

ProjectPath = sys.path[0]
ReviewArchive = path.join(ProjectPath, "ReviewArchive")
NewFolder = path.join(ProjectPath, "CompiledReview")

FileIgnore = [
	"__pycache__",
]

Rename = {
	
}

Append = [
	
]

SkippedFiles = []
Compiling = 0

def MakeDir(Directory):
	if not path.exists(Directory):
		os.makedirs(Directory)

def DeleteDir(Directory):
	if path.exists(Directory):
		shutil.rmtree(Directory)

def CopyFile(FilePath, NewPath):
	try:
		shutil.copy(FilePath, NewPath)	
	except:
		print(f'{FilePath} failed to parse.')

def FixPascalCase(String):
	NewString = ''.join(' ' + Character.lower() if Character.isupper() else Character for Character in String)

	if NewString.startswith(" "):
		NewString = NewString[1:]

	return NewString.title()

def AddParagraph(Document, Paragraph, ItemDirectory):
	ParagraphLines = 0

	try:
		if "#" in open(ItemDirectory, "r").read():
			print("Item has comments: " + ItemDirectory)

		ReviewNotes = SourceFileLoader("ReviewCompiler", ItemDirectory).load_module()
		Answers = ReviewNotes.Answers

		if len(Answers) == 0: 
			raise ValueError('Module is empty')
			
		for List in Answers:
			ParagraphLines += 1

			if isinstance(Answers, str) and Answers.startswith("poem"):
				PoemParts = Answers.split("\n\n")
				PoemInfo = PoemParts[0].split("\n")

				Paragraph.alignment = docx.enum.text.WD_PARAGRAPH_ALIGNMENT.CENTER
				
				Title = Paragraph.add_run(PoemInfo[1] + "\n")
				Title.bold = True
				Title.font.size = docx.shared.Pt(BigFontSize) 

				for ExtraPoemInfo in PoemInfo[2:]:
					Paragraph.add_run(ExtraPoemInfo + "\n").bold = True
				
				Paragraph.add_run("\n")

				for Stanza in PoemParts[1:]:
					Paragraph.add_run(Stanza.lstrip() + "\n\n")

				break

			if isinstance(List, str):
				Paragraph.add_run(List + "\n")
			elif isinstance(List[0], str):
				Paragraph.add_run(List[0]).bold = True
				Paragraph.add_run(f' - {List[1]}\n').bold
			elif isinstance(List[0], list):
				Paragraph.add_run(List[1] + "\n").bold = True
				
				for Answer in List[0]:
					Paragraph.add_run(f'- {Answer}\n')
					ParagraphLines += 1
			else:
				raise ValueError('List is not identified')
			
		return ParagraphLines
	except Exception as Error:
		print("Failed to load module,", Error, ItemDirectory)
		return False

def Scan(Directory):
	global Compiling
	Compiling += 1
	DirectoryItems = os.listdir(Directory)

	for Item in DirectoryItems:
		ItemDir = path.join(Directory, Item)
		ArchiveDir = path.join(NewFolder, path.relpath(ItemDir, ReviewArchive))

		if Item in FileIgnore or ItemDir in SkippedFiles: 
			continue

		if not "." in Item:
			MakeDir(ArchiveDir)
			threading.Thread(target=Scan, args=(ItemDir,)).start()
			continue

		if not Item.endswith(".py"):
			CopyFile(ItemDir, ArchiveDir)
			continue

		Document = docx.Document()
		Style = Document.styles['Normal']

		Font = Style.font
		Font.name = FontName
		Font.size = docx.shared.Pt(FontSize)

		Paragraph = Document.add_paragraph()
		Paragraph.style = Document.styles['Normal']

		NewItemName = None
		Modules = []

		for FilesToAppend in Append:
			if not Item in FilesToAppend[1:]:
				continue

			NewItemName = FilesToAppend[0]

			for TargetFileName in FilesToAppend:
				if TargetFileName == NewItemName:
					continue

				TargetFile = path.join(Directory, TargetFileName)

				if not path.exists(TargetFile): 
					print(f'{TargetFileName} does not exist in {Directory}')

					Modules = []
					NewItemName = None
					break
				
				Modules.append(TargetFile)

		if len(Modules) == 0:
			EnumCopy = ItemDir[:-3] + "Enum.py"
			Modules = [ItemDir]

			if path.exists(EnumCopy):
				Modules.append(EnumCopy)

		for Module in Modules:
			SkippedFiles.append(Module)

			AddParagraph(Document, Paragraph, Module)
			Paragraph.add_run("\n")

		if NewItemName == None:
			NewItemName = Item[:-3]

			if NewItemName in Rename:
				NewItemName = Rename[NewItemName]
			else:
				NewItemName = FixPascalCase(NewItemName)
		
		NewFileDir = path.join(Directory, NewItemName)
		NewFileDir = path.relpath(NewFileDir, ReviewArchive)
		NewFileDir = path.join(NewFolder, NewFileDir)
		NewFileDir = NewFileDir + ".docx"

		Document.save(NewFileDir)
	
	Compiling -= 1

if path.exists(NewFolder):
	DeleteDir(NewFolder)
	print("Deleted compiled folder")
	sys.exit(0)

MakeDir(NewFolder)

Start = time.time()
Scan(ReviewArchive)

while Compiling > 0:
	time.sleep(0)

End = time.time()

print("Finished compiling!")
print(f'Compiling took {str(End - Start)[:4]}s')
input()
