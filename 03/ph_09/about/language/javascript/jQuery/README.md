# タブパネル

## 実装

```javascript
<!doctype html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Tab Panel</title>
</head>

<body>
<style>
    #contain {
        width: 640px;
    }
    #contain > ul {
        margin: 0px;
        padding: 0px;
    }
    #contain > ul li {
        list-style-type: none;
        float: left;
        line-height: 160%;
        width: 128px;
        height: 40px;
    }
    #contain > ul li a {
        display: block;
        text-align: center;
        text-decoration: none;
        background-color: #cfc;
        color: #000;
        border: solid 1px Black;
    }
    #contain > ul li a.selected {
        background-color: #000;
        color: #fff;
    }
    #contain > div {
        border: 1px solid #c0c0c0;
        border-top: none;
        padding: 15px;
    }
</style>

<script src="http://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
<script>
    $(function() {
        var tabs = $('#contain');
        $('> ul li:first a', tabs).addClass('selected');
        $('> div', tabs).load(
            $('> ul li:first a', tabs).attr('href'));
        $('> ul li a', tabs).click(function(e) {
            if (!$(this).hasClass('selected')) {
                $('> ul li a.selected', tabs).removeClass('selected');
                $(this).addClass('selected');
                $('> div', tabs).load($(this).attr('href'));
            }
            e.preventDefault();
        });
    });
</script>

<div id="contain">
    <ul>
        <li><a href="html.html">HTML</a></li>
        <li><a href="js.txt">JavaScript</a></li>
        <li><a href="css.html">CSS</a></li>
        <li><a href="jquery.html">jQuery</a></li>
        <li><a href="php.php">PHP</a></li>
    </ul>
    <div></div>
</div>

</body>
</html>
```

## 読み込むファイル

### css.html

```bash
echo "<p>CSSは、Cascading Style Sheetsの略。</p>" > css.html
echo "<p>HTML、正しく書くとHyper Text Markup Language</p>" > html.html
echo "<p>jQueryは、avaScriptライブラリ</p>" > jquery.html
echo "JavaScriptは、オブジェクト指向スクリプト言語" > js.txt
echo "<p>初心者でも簡単に習得できるサーバーサイドスクリプト言語</p>" > php.php
```

# Google Map

```javascript
<!doctype html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Google Map</title>
    <script src="http://ajax.googleapis.com/ajax/libs/jquery/2.1.4/jquery.min.js"></script>
</head>

<body onload="initialize()">
<!-- 地図の読み込みスクリプト -->
<!-- bodyタグにonloadプロパティを足してある -->
<script src="http://maps.google.com/maps/api/js?sensor=false"></script>
<script>
    function initialize() {
        var myLatlng = new google.maps.LatLng(35.8257422,139.9132462,16);
        var myOptions = {
            zoom: 16,
            center: myLatlng,
            mapTypeId: google.maps.MapTypeId.ROADMAP
        }
        var map = new google.maps.Map(document.getElementById("map_canvas1"), myOptions);
        /*
            var map = new google.maps.Map(document.getElementById("map_canvas2"), myOptions);
            var map = new google.maps.Map(document.getElementById("map_canvas3"), myOptions);
        */
    }
</script>
<div id="map_canvas1" style="width:200px; height:200px"></div>

</body>
</html>
```