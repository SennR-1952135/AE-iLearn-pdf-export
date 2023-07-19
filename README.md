# i-learn-export

## Doel

Een leekracht kan op een eenvoudige manier leersporen exporteren zodat deze offline beschikbaar zijn.
Deze export moet 2 onderdelen bevatten, een screenshot van het leerspoor en een text-bestand met alle gelinkte data, liefst samen in 1 pdf.

## Nuttige links

wiki: https://i-learn.atlassian.net/wiki/home

dev:  https://dev.i-learn.be

test: https://test.i-learn.be

prod: https://myway.i-learn.be

example: https://myway.i-learn.be/library/18479057-51b8-4334-b963-79146848df34/

## Requirments

- gebruik authenticatie voor het controleren van juiste toegang
- screenshot en text (aangepaste JSON) samen in 1 pdf
- filter alle html tags uit de text
- hernoem uuids naar unieke ids (start bij 1)
- vertaal keys
- klikbare hyperlinks