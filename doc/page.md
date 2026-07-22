# Pages, Sessions, Application and Servers

A server is capable of serving several applications thanks to different URL.
An application is basically made of an index page possibly followed by other
pages.

In the case of a server running forever servicing its application, the
different connections are represented by sessions: for each HTTP connection
to an application, a session is created that will provides its own set
of pages. When all pages of a session are closed, the session is also closed.

In the special case of an application not running as a server, the closure
of the unique session causes the halt of the server. Therrefore, Orchid
can run as:
* a lonely application: 1 application, 1 session, a set of pages, stopped
	as soon all pages are closed.
* a server: _n_ application having _m_ sessions with _k_ pages and never
	stops.


## Starting Orchid

Basically using **Orchid** requires to create an `Application` whose index page
is passed as parameter `first` to the constructor. To run the application,
the function `run` is called with parameters passed to the server:

* `debug`: if true, display debugging messages.
* `host`: name of the host (else `localhost`).
* `port`: port to use (else defined automatically).
* `dirs`: list of directories to find assets (images, HTML, etc).
* `browser`: if true, display the application page in the default browser.
* `server`: if true, run as a server (does not stop).
* `session_timeout`: time-out to close the session without activity (in s).
* `proxy`: if **Orchid** runs behind a proxy, its address (to correctly generate the URLs).


## Liefecycle of Pages and Sessions

When the function `run`is called, a server starts serving pages of the application.

 When an HTTP connection is performed, a session is created and the _first_ page
is generated and returned.

(A) The session tracks the activity of the remote user: each time there is an interaction
in the remote page causing a message to be issued to the server, the date is _updated_,
recorded in the session. In parallel, there is a daemon running to test
session without activity. When the last activity date and the current is bigger than
`session_timeout`, the session is considered exhausted and remove from the **Orchid**.
The function `Session.release()` is called to let server and application release
resources of the session.

(B) A second cause of session closure may come from the remote page: the page is closed
in the browser. In this case, a `close` signal is send to the page causing a call
to `Page.on_close()` function. The page itself alerts the session of the closure
of the page with `Session.remove_page()`.

(C) Finally closure may come from the application by calling `Page.close()`. This
behaviour is always the result of a request from the remote page and the answer
result in a `quit` message that, in turn, turn to be the same as case (B),
with a small difference that, sometimes, the closing message from the remote
page cannot come back (depending on the behaviour of the remote browser).
This is why the closing message wait is limited by a time-out `CLOSE_TIMEOUT`
of 250ms.

This workflow usually supports all cases except the _Reload_ case. From the point
of view of the remote page, there is currently no way to make the difference
with a classic page closure. So when the page is reloaded, a _closure_ message
is send to the server. To let a chance to reload the page (without releasing
the session), the page closure is delayed during `CLOSE_DELAY` i.e. 3s. So, if
the page is requested before the end of the delay, this is considered as a
_reload_ and the page is no more considered closing.


## Server and Providers



