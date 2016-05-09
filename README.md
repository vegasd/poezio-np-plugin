# poezio-np-plugin
Plugin for poezio IM for sending now playing messages to conferences

There is only russian version of messages at this moment.

Only deadbeef player is supported at this moment.

Пока (?) только русская версия сообщений.

Плагин добавляет команду /np, позволяющую отправлять в чат красиво оформленное
сообщение о прослушиваемой на в данный момент композиции в плеере (пока только
deadbeef). Учитываются особенности релизов, типы треков и т. д.

## Installation

Just put *np.py* to .local/share/poezio/plugins, then you can load the plugin
with `/load np`. You can also add 'np' to *autoload* in poezio config.

## Usage

`/np` command will send a message to current MUC. You can also add a comment
which will be appended to the end of this message: `/np , мне нравится`.
