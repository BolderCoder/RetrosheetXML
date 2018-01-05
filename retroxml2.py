#!/usr/bin/env python
import xml.etree.ElementTree as ET
import sys
import datetime
# import nltk as NL

Positions = {"0": "DH", "1": "P", "2": "C", "3": "1B", "4": "2B", "5": "3B", "6": "SS", "7": "LF", "8": "CF", "9": "RF"
             , "ph": "PH", "pr": "PR", "dh": "DH"}
DaysOfTheWeek = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

FileName = sys.argv[1]
# FileName = 'ANA'

Header = "Date,DOW,Team,Opp,Site,Key,Last,"
Header = Header + "First,Pos,BatOrder,"
Header = Header + "PAs,"
Header = Header + "ABs,"
Header = Header + "RUNs,"
Header = Header + "Singles,"
Header = Header + "Doubles,"
Header = Header + "Triples,"
Header = Header + "HRs,"
Header = Header + "RBIs,"
Header = Header + "Ks,"
Header = Header + "BOBs,"
Header = Header + "IWs,"
Header = Header + "HBPs,"
Header = Header + "SBs,"
Header = Header + "SBCs,"
Header = Header + "SacFlies,"
Header = Header + "SacBunts,"
Header = Header + "GIDPs,"
Header = Header + "TBs,"
Header = Header + "DKSc"
if FileName == "ANA":
    print(Header)
FileName = '/home/bill/retrosheet/2017/out/' + FileName + '.XML'
tree = ET.parse(FileName)

root = tree.getroot()

for games in root:
    DateOfGame = ""
    DayOfWeek = ""
    Year = 0
    Month = 0
    Day = 0

    HomeTeam = ""
    AwayTeam = ""
    Site = ""
    Team1 = ""
    Team2 = ""
    Opp = ""

    for gamemeta in games:

        for gamedata in gamemeta:
            CurrentTeam = ""
            if gamedata.tag == "event-metadata":
                DateOfGame = gamedata.attrib['start-date-time'][:8]
                Year = int(DateOfGame[:4])
                Month = int(DateOfGame[4:6])
                Day = int(DateOfGame[6:])
                DayOfWeek = DaysOfTheWeek[datetime.date(Year, Month, Day).weekday()]

            for gameinfo in gamedata:
                try:
                    if gameinfo.tag == "sports-content-code" and gameinfo.attrib.get('code-type') == 'team':
                        if Team1 == '':
                            Team1 = gameinfo.attrib.get('code-key')
                        else:
                            Team2 = gameinfo.attrib.get('code-key')

                except OSError:
                    DoNothing = ""

                if gameinfo.tag == "team-metadata":
                    if gameinfo.attrib['alignment'] == "away":
                        AwayTeam = gameinfo.attrib['team-key']
                    else:
                        HomeTeam = gameinfo.attrib['team-key']

                    CurrentTeam = gameinfo.attrib['team-key']

                if gameinfo.tag == "site-metadata":
                    Site = gameinfo.attrib['site-key']

                for gamedetails in gameinfo:
                    if gamedetails.tag == "site-metadata":
                        Site = gamedetails.attrib['site-key']

                    if gamedetails.tag == "player-metadata":
                        PlayerKey = gamedetails.attrib["player-key"]
                        FieldPosition = gamedetails.attrib["position-event"]
                        FPos = Positions[FieldPosition]
                        PlayerStatus = gamedetails.attrib["status"]
                        LineupSlot = gamedetails.attrib["lineup-slot"]

                    for gamestats in gamedetails:
                        if gamestats.tag == "name":
                            PlayerFirst = gamestats.attrib["first"]
                            PlayerLast = gamestats.attrib["last"]

                        for gamestatsdetail in gamestats:
                            if gamestatsdetail.tag == "stats-baseball-offensive":
                                Singles = gamestatsdetail.attrib['singles']
                                Doubles = gamestatsdetail.attrib['doubles']
                                Triples = gamestatsdetail.attrib['triples']
                                HRs = gamestatsdetail.attrib['home-runs']
                                PAs = gamestatsdetail.attrib['plate-appearances']
                                ABs = gamestatsdetail.attrib['at-bats']
                                Ks = gamestatsdetail.attrib['strikeouts']
                                RBIs = gamestatsdetail.attrib['rbi']
                                RUNs = gamestatsdetail.attrib['runs-scored']
                                BOBs = gamestatsdetail.attrib['bases-on-balls']
                                IWs = gamestatsdetail.attrib['bases-on-balls-intentional']
                                HBPs = gamestatsdetail.attrib['hit-by-pitch']
                                SBs = gamestatsdetail.attrib['stolen-bases']
                                SBCs = gamestatsdetail.attrib['stolen-bases-caught']
                                GIDPs = gamestatsdetail.attrib['grounded-into-double-play']
                                TBs = gamestatsdetail.attrib['total-bases']
                                SacFlies = gamestatsdetail.attrib['sac-flies']
                                SacBunts = gamestatsdetail.attrib['sac-bunts']
                                DraftKingScore = (int(Singles) * 3) + (int(Doubles) * 5) + (int(Triples) * 8) + (int(HRs) * 10)
                                DraftKingScore = DraftKingScore + (int(HRs) * 10) + (int(RBIs) * 2) + (int(RUNs) * 2)
                                DraftKingScore = DraftKingScore + (int(BOBs) * 2) + (int(HBPs) * 2)
                                DraftKingScore = DraftKingScore + (int(SBs) * 2)

                                if CurrentTeam == Team1:
                                    Opp = Team2
                                else:
                                    Opp = Team1

                                ShowLine = DateOfGame + "," + DayOfWeek + "," + CurrentTeam + "," + Opp + ","
                                ShowLine = ShowLine + Site + "," + PlayerKey + "," + PlayerLast + ","
                                ShowLine = ShowLine + PlayerFirst + "," + FPos + "," + LineupSlot + ","
                                ShowLine = ShowLine + PAs + ","
                                ShowLine = ShowLine + ABs + ","
                                ShowLine = ShowLine + RUNs + ","
                                ShowLine = ShowLine + Singles + ","
                                ShowLine = ShowLine + Doubles + ","
                                ShowLine = ShowLine + Triples + ","
                                ShowLine = ShowLine + HRs + ","
                                ShowLine = ShowLine + RBIs + ","
                                ShowLine = ShowLine + Ks + ","
                                ShowLine = ShowLine + BOBs + ","
                                ShowLine = ShowLine + IWs + ","
                                ShowLine = ShowLine + HBPs + ","
                                ShowLine = ShowLine + SBs + ","
                                ShowLine = ShowLine + SBCs + ","
                                ShowLine = ShowLine + SacFlies + ","
                                ShowLine = ShowLine + SacBunts + ","
                                ShowLine = ShowLine + GIDPs + ","
                                ShowLine = ShowLine + TBs + ","
                                ShowLine = ShowLine + str(DraftKingScore)
                                if int(LineupSlot) > 0 and FPos != "P" and PlayerStatus == "starter":   # batter?
                                    print(ShowLine)

    # print(DateOfGame + " - " + AwayTeam + " @ " + HomeTeam + " Playing in " + Site)
