const parseQueryString = url => {
    let json = {};
    let arr = url.substr(url.indexOf('?') + 1).split('&');
    arr.forEach(item => {
        let tmp = item.split('=');
        json[tmp[0]] = decodeURI(decodeURI(tmp[1]));
    });
    return json;
};

new Vue({
    el: "#main",
    mounted: function () {
        axios.get('/blog/posts/manifest.json').then(response => {
            this.posts = response.data;
            this.params = parseQueryString(window.location.search);
            this.id = Number(this.params.id);
            this.post = this.posts.filter(post => post.id == this.id)[0];
            console.log(this.post);
            axios.get('/blog/posts/' + this.post.target).then(response => {
                this.content = response.data;
            });
            let getPostPrevious = posts =>
                posts.filter(post => post.id < this.post.id)
                    .reduce((prev, now) => (!prev || now.id > prev.id) ? now : prev, undefined)
            this.postPrevious = getPostPrevious(this.posts);

            let getPostNext = posts =>
                posts.filter(post => post.id > this.post.id)
                    .reduce((next, now) => (!next || now.id < next.id ? now : next), undefined)
            this.postNext = getPostNext(this.posts);
        });
    },
    updated: () => {
        renderMathInElement(document.body, {
            delimiters: [
                { left: "$$", right: "$$", display: true },
                { left: "$", right: "$", display: false },
                { left: "\\(", right: "\\)", display: false },
                { left: "\\[", right: "\\]", display: true }
            ]
        });
    },
    data: {
        id: 0,
        params: {},
        posts: [],
        post: {},
        content: undefined,
        postPrevious: undefined,
        postNext: undefined,
    },
    methods: {
        id2link: function (id) {
            return id ? '/blog/post.html?id=' + id : undefined;
        }
    }
});
