/*a set of handy functional js tools
 * a work in progress :)
 *
 */
var BASE_TEN = 10;
var EXPECTED_TIME_LENGTH = 3

function formatDate(date, pattern){
    /*
     * takes json string date from django datetime object and returns a
     * formatted Extjs date object
     */
    var date = jsDateFromString(date)
    return date.format(pattern);
}


function jsDateFromString(date){
    /*
     * takes a datetime string formated as json from python/django and returns a
     * JS Date object
     */
    var split1 = date.split(' ');// '2009-12-10 23:14:42' becomes [y-m-d,
                                    // time]
    
    var date = split1[0].split('-');// results in [y,m,d]
    
    var year = parseInt(date[0], BASE_TEN);// first item in the date array,
                                            // passed
                                        // to parse int with base 10 as an
                                        // argument
    var month = parseInt(date[1], BASE_TEN) -1;// new Date expects 0-11 for
                                                // month
    var day = parseInt(date[2], BASE_TEN);
    
    if (split1[1]){
        var time = split1[1].split(':');// results in [hour,minute,second]
        if(!time.length === EXPECTED_TIME_LENGTH){
            return undefined;
        }
        var hour = parseInt(time[0], BASE_TEN);
        var minute = parseInt(time[1], BASE_TEN);
        var second = parseInt(time[2], BASE_TEN);
        
    }
    else{
        var hour = 0;
        var minute = 0;
        var second = 0;
    }
    
    return new Date(year, month, day, hour, minute, second);
}


function title(sentence){
    /* title("get it while it's hot") = "Get It While It's Hot" */
    
    var arr = sentence.split(" ");
    var ret = "";
    for (var i = 0; arr.length; i++) {
        ret += capWord(arr[i]);
        if (!i == len - 1) {
            ret += " ";
        }
    }
    return ret;
}


function capWord(str){
    // capWord("bill") = "Bill"
    return str.substring(0, 1).toUpperCase() + str.substring(1);
}


function getTimeSeed(){
    // utility function for randomizing widget id's
    return Date.UTC(2009, new Date().getMilliseconds());
}


function size(obj){
    // returns the number of keys in an object..(size)
    
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) 
            size++;
    }
    return size;
};


function isArray(obj){
    // returns true if the object pass is an instance of Array
    if (obj.constructor.toString().indexOf("Array") == -1) 
        return false;
    else 
        return true;
}

function toArray(nodes){
    // used for a return value from .getElementsBy*, these values aren't true
    // arrays, this makes them so
    try {
        // most browsers support array.prototype.slice
        var arr = Array.prototype.slice.call(nodes);
        return arr;
    } 
    catch (err) {
        // those that don't we do it the old fashion way
        var arr = [], length = nodes.length;
        for (var i = 0; i < length; i++) {
            arr.push(nodes[i]);
        }
        return arr;
    }
}


function isEven(num){
    if (typeof(num) !== 'number') {
        throw TypeError(num + " is not a number");
    }
    else {
        return (num % 2 == 0);
    }
}

Array.prototype.filter = function(test){
    /*
     * Filters an array down for which the objects return true for the given
     * test
     */
    var ret = [];
    for (var i = 0; i < this.length; i++) {
        if (test(this[i]) == true) {
            ret.push(this[i])
        }
    }
    return ret;
}


Array.prototype.flatten = function(){
    /*
     * accepts an array of arrays, returning a single, flattened array e.g.
     * flatten([1,2],3,[4,5]) = [1,3,4,5]
     */
    var ret = []
    function _flatten(arr){
        for (var i = 0; i < arr.length; i++) {
            // check if the data at index i is an array
            // if not, just stick it on the result
            if (isArray(arr[i]) != true) {
                ret.push(arr[i])
            }
            else {
                // it is an array, so push it back into the _flatten to flatten
                // deeper
                _flatten(arr[i]);
            }
        }
        return ret;
    }
    return _flatten(this);
}

Array.prototype.max = function(){
    if (this.length == 0) {
        return undefined;
    }
    var max = this[0];
    for (var i = 1; i < this.length; i++) {
        if (this[i] > max) {
            max = this[i];
        }
    }
    return max;
};

Array.prototype.min = function(){
    if (this.length == 0) {
        return undefined;
    }
    var min = this[0];
    var len = this.length;
    for (var i = 1; i < len; i++) {
        if (this[i] < min) {
            min = this[i];
        }
    }
    return min;
};

Array.prototype.includes = function(k){
    for (var i = 0; i < this.length; i++) {
        if (this[i] == k) {
            return true;
        }
    }
    return false;
};


Array.prototype.next = function(item){
    var index = this.indexOf(item)
    return this[index + 1];
    
}


Array.prototype.remove = function(item){
    if (!this.includes(item)){
        return;
    }
    for (var i=0;i<this.length;i++){
        if (this[i] == item){
            this.splice(i, 1);
            return this;
        }
        
    }
    
}

Array.prototype.set = function(){
/* returns a unique version of the array */
    var ret = [];
    for (var i = 0; i < this.length; i++) {
        if (!includes(ret, this[i])) {
            ret.push(this[i]);
        }
     }
        return ret;
    
    
}

if(!Array.indexOf){
// if type Array doesn't have an indexOf method (in IE), we add it, this returns
// the
// index in the array of the passed value, -1 in case of it not existing
    Array.prototype.indexOf = function(obj){
        for (var i=0;i<this.length;i++){
            if(this[i]==obj){
                return i;
            }
        }
        return -1;
    }

}

Object.size = function(obj){
    var size = 0, key;
    for (key in obj) {
        if (obj.hasOwnProperty(key)) 
            size++;
    }
    return size;
};

chain = function(){
    for (var i = 0; i < arguments.length; i++) {
        agruments[i]();
    }
};


function get_previoussibling(node){
    // allows you to get the previous sibling only if it is a div or span,
    // ignoring 'false' textnodes
    x = node.previousSibling;
    while (x.nodeType != 1) {
        x = x.previousSibling;
    }
    return x;
}

function object(o){
    function F(){}
    F.prototype = o;
    return new F();
}


// Remove whitespace characters from the beginning and end of a string
function trim(str, chars) {
return ltrim(rtrim(str, chars), chars);
}

/* Remove whitespace characters from the beginning of a string */
function ltrim(str, chars) {
chars = chars || "\\s";
return str.replace(new RegExp("^[" + chars + "]+", "g"), "");
}

/* Remove whitespace characters from the end of a string */
function rtrim(str, chars) {
chars = chars || "\\s";
return str.replace(new RegExp("[" + chars + "]+$", "g"), "");
}


/*
 * Starts with and endswith 'foobar'.startsWith('foo') == true;
 * 'foobar'.endsWith('bar') == true;
 */

String.prototype.startsWith = function(str){
    return (this.match("^"+str)==str);
}

String.prototype.endsWith = function(str){
    return (this.match(str+"$")==str);
}


String.prototype.strFormat = function(){
/*
 * string formating method in the spirit of python allows you to pass an
 * arbitrary number of arguments to replace tokens in a tokenized string
 * 
 * e.g: "<class="{0}" id="{1}">'.strFormat('foo', 'bar') // "<a class="foo"
 * id="bar">"
 * 
 */
     var args = toArray(arguments)
     return this.replace(/\{(\d+)\}/g, function(match, idx){ return args[idx] });
}


String.prototype.reverse=function(){
    // reverses a string
    return this.split("").reverse().join("");
}

function range(low, high, step) {
// return a numeric list with the given params
// will increment by optional step argument
    var result = [];
    for(var i=low;i <= high; i+=step){
       result.push(i);
    }
    return result;
}   


function setSelectionValue(selectObjectName, value) {
    selectObject = document.getElementById(selectObjectName);
    
    if(!selectObject)
        return;
    
    for(var i=0; i< selectObject.length; i++) {
        if(selectObject[i].value == value){
            selectObject.selectedIndex = i;
            return;
        }
    }
}


function setRadioValue(radioObjects, value) {   
    if(!radioObjects)
        return;
    
    for(var i=0; i< radioObjects.length; i++) {
        if(radioObjects[i].value == value){
            radioObjects[i].checked = true;
        }
        else {
            radioObjects[i].checked = false;
        }
    }
}


Date.prototype.date = function(){
    // mimics python's .date() function, returns a value of a date devoid of any
    // time information
    // useful for comparing two days when you aren't interested in the time
    // ie: you want to see if Jan 7, 2010 6:15 and Jan 7, 2010 4:31 are on the
    // same day
    return new Date(this.getFullYear(), this.getMonth(), this.getDate());
}


if('function' !== typeof RegExp.escape) {
    /**
     * Escapes regular expression
     * @param {String} s
     * @return {String} The escaped string
     * @static
     */
    RegExp.escape = function(s) {
        if('string' !== typeof s) {
            return s;
        }
        return s.replace(/([.*+?\^=!:${}()|\[\]\/\\])/g, '\\$1');
    };
}