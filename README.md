# poezio-np-plugin
Plugin for poezio IM for sending now playing messages to conferences

There is only russian version of messages at this moment.

Only deadbeef player is supported at this moment.

Also can be used as standalone program.

Пока (?) только русская версия сообщений.

Плагин добавляет команду /np, позволяющую отправлять в чат красиво оформленное
сообщение о прослушиваемой на в данный момент композиции в плеере (пока только
deadbeef). Учитываются особенности релизов, типы треков и т. д.

## Plugin installation

Just put *np.py* to .local/share/poezio/plugins, then you can load the plugin
with `/load np`. You can also add 'np' to *autoload* in poezio config.

## Plugin usage

`/np` command will send a message to current MUC. You can also add a comment
which will be appended to the end of this message: `/np , мне нравится`.

## Standalone usage

You can just run `./np.py`. To get now-playing message to your stdout.

To get it in your clipboard you can do something like

````sh
./np.py | xclip
````
