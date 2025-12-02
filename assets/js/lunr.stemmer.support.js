/*!
 * Snowball JavaScript Library v0.3
 * http://code.google.com/p/urim/
 * http://snowball.tartarus.org/
 *
 * Copyright 2010, Oleg Mazko
 * http://www.mozilla.org/MPL/
 */
!function (r, t) {
    "function" == typeof define && define.amd
        ? define(t)
        : "object" == typeof exports
        ? module.exports = t()
        : t()(r.lunr);
}(this, function () {
    return function (r) {
        var t = r.stemmerSupport = {},
            e = new RegExp("^[\\s\\S]*$");

        t.clear = function (r) {
            return e = new RegExp(r);
        };

        t.generateTrimmer = function (e) {
            return function (r) {
                return r.update(function (r, t) {
                    return r
                        .trim()
                        .toLowerCase()
                        .replace(new RegExp("((?!^).)(?=" + e + ")", "g"), "$1\n")
                        .split("\n");
                });
            };
        };

        t.trimmer = t.generateTrimmer("");

        r.Pipeline.registerFunction(t.trimmer, "trimmer-support");
    };
})();