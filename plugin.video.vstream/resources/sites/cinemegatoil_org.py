#-*- coding: utf-8 -*-
# https://github.com/Kodi-vStream/venom-xbmc-addons
from resources.lib.gui.hoster import cHosterGui
from resources.lib.gui.gui import cGui
from resources.lib.handler.inputParameterHandler import cInputParameterHandler
from resources.lib.handler.outputParameterHandler import cOutputParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.parser import cParser
from resources.lib.comaddon import progress

UA = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:60.0) Gecko/20100101 Firefox/60.0'

SITE_IDENTIFIER = 'cinemegatoil_org'
SITE_NAME = 'CineMegaToil'
SITE_DESC = 'Films - Films HD'

URL_MAIN = 'https://www.cinemegatoil.org/'

MOVIE_NEWS = (URL_MAIN + 'film', 'showMovies')
MOVIE_MOVIE = ('http://', 'load')
MOVIE_GENRES = (True, 'showGenres')

URL_SEARCH = (URL_MAIN + '?do=search&mode=advanced&subaction=search&titleonly=3&story=', 'showMovies')
URL_SEARCH_MOVIES = (URL_MAIN + '?do=search&mode=advanced&subaction=search&titleonly=3&story=', 'showMovies')

def load():
    oGui = cGui()

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', 'http://venom/')
    oGui.addDir(SITE_IDENTIFIER, 'showSearch', 'Recherche', 'search.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_NEWS[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_NEWS[1], 'Films (Derniers ajouts)', 'news.png', oOutputParameterHandler)

    oOutputParameterHandler = cOutputParameterHandler()
    oOutputParameterHandler.addParameter('siteUrl', MOVIE_GENRES[0])
    oGui.addDir(SITE_IDENTIFIER, MOVIE_GENRES[1], 'Films (Genres)', 'genres.png', oOutputParameterHandler)


    oGui.setEndOfDirectory()

def showSearch():
    oGui = cGui()

    sSearchText = oGui.showKeyBoard()
    if (sSearchText != False):
        sUrl = sSearchText
        showMovies(sUrl)
        oGui.setEndOfDirectory()
        return

def showGenres():
    oGui = cGui()

    liste = []
    liste.append( ['Action', URL_MAIN + 'action'] )
    liste.append( ['Animation', URL_MAIN + 'animation'] )
    liste.append( ['Arts-martiaux', URL_MAIN + 'arts-martiaux'] )
    liste.append( ['Aventure', URL_MAIN + 'aventure'] )
    liste.append( ['Biopic', URL_MAIN + 'biopic'] )
    liste.append( ['Comédie', URL_MAIN + 'comedie'] )
    liste.append( ['Comédie musicale', URL_MAIN + 'comedie-musicale'] )#l'url sur le site n'est pas bonne
    liste.append( ['Documentaire', URL_MAIN + 'documentaire'] )
    liste.append( ['Drame', URL_MAIN + 'drame'] )
    liste.append( ['Epouvante-horreur', URL_MAIN + 'epouvante-horreur'] )
    liste.append( ['Espionnage', URL_MAIN + 'espionnage'] )
    liste.append( ['Exclu', URL_MAIN + 'exclu'] )
    liste.append( ['Famille', URL_MAIN + 'famille'] )
    liste.append( ['Fantastique', URL_MAIN + 'fantastique'] )
    liste.append( ['Guerre', URL_MAIN + 'guerre'] )
    liste.append( ['Historique', URL_MAIN + 'historique'] )
    liste.append( ['Musical', URL_MAIN + 'musical'] )
    liste.append( ['Policier', URL_MAIN + 'policier'] )
    liste.append( ['Romance', URL_MAIN + 'romance'] )
    liste.append( ['Science-fiction', URL_MAIN + 'science-fiction'] )
    liste.append( ['Thriller', URL_MAIN + 'thriller'] )
    liste.append( ['Vieux Film', URL_MAIN + 'vieux-film'] )
    liste.append( ['Western', URL_MAIN + 'western'] )

    for sTitle, sUrl in liste:

        oOutputParameterHandler = cOutputParameterHandler()
        oOutputParameterHandler.addParameter('siteUrl', sUrl)
        oGui.addDir(SITE_IDENTIFIER, 'showMovies', sTitle, 'genres.png', oOutputParameterHandler)

    oGui.setEndOfDirectory()

def showMovies(sSearch = ''):
    oGui = cGui()
    oParser = cParser()

    if sSearch:
        if URL_SEARCH[0] in sSearch:
            sUrl = sSearch
        else:
            sUrl = URL_SEARCH[0] + sSearch
        sUrl = sUrl.replace(' ','+')
    else:
        oInputParameterHandler = cInputParameterHandler()
        sUrl = oInputParameterHandler.getValue('siteUrl')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()

    sPattern = '<div class="poster.+?img src="([^"]+)".+?<div class="quality">(.+?)<\/div>.+?<div class="title"><a href="([^"]+)".+?title="(.+?)".+?<li class="label">Ann.+?<li>(.+?)</li>.+?<div class="shortStory">(.+?)</div>'
    aResult = oParser.parse(sHtmlContent, sPattern)

    if (aResult[0] == False):
        oGui.addText(SITE_IDENTIFIER)

    if (aResult[0] == True):
        total = len(aResult[1])
        progress_ = progress().VScreate(SITE_NAME)

        for aEntry in aResult[1]:
            progress_.VSupdate(progress_, total)
            if progress_.iscanceled():
                break

            sUrl2 = aEntry[2]
            sThumb = aEntry[0]
            if sThumb.startswith('//'):
                sThumb = 'http:' + sThumb

            sTitle = aEntry[3]
            sQual = aEntry[1]
            sYear = aEntry[4]
            sDesc = aEntry[5]
            sDisplayTitle = ('%s [%s] (%s)') % (sTitle, sQual, sYear)

            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sUrl2)
            oOutputParameterHandler.addParameter('sMovieTitle', sTitle)
            oOutputParameterHandler.addParameter('sThumb', sThumb)
            oGui.addMovie(SITE_IDENTIFIER, 'showHosters', sDisplayTitle, 'films.png', sThumb, sDesc, oOutputParameterHandler)

        progress_.VSclose(progress_)

        sNextPage = __checkForNextPage(sHtmlContent)
        if (sNextPage != False):
            oOutputParameterHandler = cOutputParameterHandler()
            oOutputParameterHandler.addParameter('siteUrl', sNextPage)
            oGui.addNext(SITE_IDENTIFIER, 'showMovies', '[COLOR teal]Next >>>[/COLOR]', oOutputParameterHandler)

    if not sSearch:
        oGui.setEndOfDirectory()

def __checkForNextPage(sHtmlContent):
    sPattern = '<span class="prev-next">.+?href="([^"]+)">'
    oParser = cParser()
    aResult = oParser.parse(sHtmlContent, sPattern)
    if (aResult[0] == True):
        return  aResult[1][0]

    return False

def showHosters():
    oGui = cGui()
    oParser = cParser()
    oInputParameterHandler = cInputParameterHandler()
    sUrl = oInputParameterHandler.getValue('siteUrl')
    sMovieTitle = oInputParameterHandler.getValue('sMovieTitle')
    sThumb = oInputParameterHandler.getValue('sThumb')

    oRequestHandler = cRequestHandler(sUrl)
    sHtmlContent = oRequestHandler.request()
    #Vire les bandes annonces
    sHtmlContent = sHtmlContent.replace('src="https://www.youtube.com/', '')
    
    #sHtmlContent = oParser.abParse(sHtmlContent, '<div class="tcontainer video-box">', '<div class="tcontainer video-box" id=')
    
    sPattern = 'src=\'([^\']+)\''
    aResult = oParser.parse(sHtmlContent, sPattern)
    if not aResult[0] == True:
        sPattern = '<div class="dllink"><a href="([^"]+)"'
        aResult = oParser.parse(sHtmlContent, sPattern)
        
    if (aResult[0] == True):
        for aEntry in aResult[1]:

            if '//goo.gl' in aEntry:
                import urllib2
                try:
                    class NoRedirection(urllib2.HTTPErrorProcessor):
                        def http_response(self, request, response):
                            return response

                    url8 = aEntry.replace('https', 'http')

                    opener = urllib2.build_opener(NoRedirection)
                    opener.addheaders.append (('User-Agent', UA))
                    opener.addheaders.append (('Connection', 'keep-alive'))

                    HttpReponse = opener.open(url8)
                    sHosterUrl = HttpReponse.headers['Location']
                    sHosterUrl = sHosterUrl.replace('https', 'http')
                except:
                    pass
            else:
                sHosterUrl = aEntry

            oHoster = cHosterGui().checkHoster(sHosterUrl)
            if (oHoster != False):
                oHoster.setDisplayName(sMovieTitle)
                oHoster.setFileName(sMovieTitle)
                cHosterGui().showHoster(oGui, oHoster, sHosterUrl, sThumb)

    oGui.setEndOfDirectory()
