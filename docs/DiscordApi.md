# Предисловие
Данная статья - краткое описание работы с dicord python library на русском языке,
 являющаяся вольным переводом официальной [документации](https://discordpy.readthedocs.io/en/latest/intro.html#basic-concepts)
 
 
# Basic Concepts
Библиотека является оберткой вокруг событий,
 которые вы из кода можете прослушивать и соответственно реагировать.
Каждое событие передается в соответствующий метод класса discord.Client.
Клиент и вся библиотека написана в асинхронном стиле, поэтому вам необходимо 
владеть базовыми понятиями [asyncio](https://habr.com/ru/post/453348/)

Ниже приведен простой пример, иллюстрирующий это.
Новый класс MyClient переопределяет соответствующие методы событий:

* Метод `on_ready` вызывается при завершениии процессов авторизации и прочих. 
    Не гарантируется, что он будет вызываться всегда.
 
* Метод `on_message` вызывается при появлении новых сообщений. 
**Важно:** _вызывается при любых новых сообщениях, в том числе и своих 
собственных, легко попасть в рекурсию))_

* Метод `run` запускает клиент чз loop из asyncio 

```python
import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client = MyClient()
client.run('my token goes here')
```

# Клиент

Я выписал наиболее употребительные свойства для клиента.
Все методы, соответствующие событиям, являются асинхронными.  
Методы:
* `run` - запускает клиент чз loop из asyncio. 
    Вообще говоря, это бесконечный цикл, который крутится всю программу,
    поэтому весь код поле вызова run будет вам недоступен в клиенте.
    Принимает token доступа для подключения клиента.  
    **Kwargs**: 
    - `bot = True` - на stackoverflow указывали, что при подключении клиента 
как юзера, нужно указывать False. _Это прокидываемый параметр в метод login_
Обратите внимание, что в таком случае ваш аккаунт может быть 
[забанен](https://support.discord.com/hc/en-us/articles/115002192352)

* `get_channel(id)`, `get_guild(id)`

# События
  * `on_typing(channel, user, when)`
  * `on_message(message)`
  * `on_message_edit(before, after)`
  before, after - старая и текущая версии сообщения.
  Это событие может быть не вызвано, если соответсвующего
  сообщения не нашлось в кэше клиента 

# Сообщения
Свойства у сообщений, предаваемых on_message
* properties
    - id
    - author
    - content
    - channel - обьект канала
    - guild - обьект гильдии
    - created_at - время создания [_datetime.datetime_]
    - mentions - List[abc.User]  
    Упоминание пользователей в сообщении,
     список не упорядоченный в порядке упоминания
* methods  
    - `await delete(*, delay=None)`  
       удалить сообщение
    - `await edit(**fields)`  
        отредактировать сообщение

# TextChannel
Поддерживает операции ==, !=, str() -> name
* properties
    - id
    - name
    - guild  
* methods  
    - `async for ... in history(*, limit=100, before=None, after=None, around=None, oldest_first=None)`
    - `async with typing()`
    - `await send(content=None, *, tts=False, embed=None, file=None, files=None, delete_after=None, nonce=None, allowed_mentions=None)`  
        Возвращает опубликованное сообщение
