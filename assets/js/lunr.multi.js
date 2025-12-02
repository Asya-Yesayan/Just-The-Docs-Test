!function (e, t) {
    "function" == typeof define && define.amd
        ? define(t)
        : "object" == typeof exports
        ? module.exports = t()
        : t()(e.lunr);
}(this, function () {
    return function (e) {
        e.multiLanguage = function () {
            var t = Array.prototype.slice.call(arguments),
                i = t.join("-"),
                r = "",
                n = [],
                s = [];

            for (var p = 0; p < t.length; ++p) {
                if ("en" == t[p]) {
                    r += "\\w";
                    n.unshift(e.stopWordFilter);
                    n.push(e.stemmer);
                    s.push(e.stemmer);
                } else {
                    r += e[t[p]].wordCharacters;
                    e[t[p]].stopWordFilter && n.unshift(e[t[p]].stopWordFilter);
                    e[t[p]].stemmer && (n.push(e[t[p]].stemmer), s.push(e[t[p]].stemmer));
                }
            }

            var o = e.trimmerSupport.generateTrimmer(r);
            e.Pipeline.registerFunction(o, "lunr-multi-trimmer-" + i);
            n.unshift(o);

            return function () {
                this.pipeline.reset();
                this.pipeline.add.apply(this.pipeline, n);

                if (this.searchPipeline) {
                    this.searchPipeline.reset();
                    this.searchPipeline.add.apply(this.searchPipeline, s);
                }
            };
        };
    };
});
