[Setup]
AppName=Ali-Scrape
AppVersion=1.0
DefaultDirName={pf}\Ali-Scrape
UninstallDisplayName=Ali-Scrape
OutputDir=.
Compression=lzma2
SolidCompression=yes

[Files]
Source: "dist\Ali-Scrape.exe"; DestDir: "{app}"
Source: "chromedriver.exe"; DestDir: "{app}"
Source: "chromedriver"; DestDir: "{app}"
