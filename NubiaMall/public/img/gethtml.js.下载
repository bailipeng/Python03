// Old compatibility code, no longer needed.
if (window.XMLHttpRequest) { // Mozilla, Safari, IE7+ ...
    httpRequest = new XMLHttpRequest();
} else if (window.ActiveXObject) { // IE 6 and older
    httpRequest = new ActiveXObject("Microsoft.XMLHTTP");
}

httpRequest.onreadystatechange = function(){
    // process the server response
    if (httpRequest.readyState === XMLHttpRequest.DONE) {
      if (httpRequest.status === 200) {
        document.write(httpRequest.responseText);
      } else {
        alert('There was a problem with the request.');
      }
    }
};

httpRequest.open('GET', '/htmlhelp.php?a=gethtml', false); //true为异步，false为同步，默认为异步
httpRequest.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
httpRequest.setRequestHeader('Cache-Control', 'max-age=600');
httpRequest.send(null);