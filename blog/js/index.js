new Vue({
    el:"#main",
    mounted: function() {
        axios.get('/blog/posts/manifest.json').then((response)=>{
            this.posts=response.data.sort((a,b)=>a.id<b.id);
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
        posts:[],
    },
})