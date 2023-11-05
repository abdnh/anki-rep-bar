function _addOrRemoveRepBarBorder() {
    const bar = document.getElementById("rep-bar");
    bar.classList.toggle(
        "bordered",
        bar.children.length * 12 <= document.documentElement.clientWidth,
    );
}

window.addEventListener("resize", () => {
    _addOrRemoveRepBarBorder();
});

function addRepBlocks(remaining, passed) {
    const bar = document.getElementById("rep-bar");
    bar.innerHTML = "";

    function createBlock() {
        const block = document.createElement("div");
        block.classList.add("rep-block");
        bar.appendChild(block);
        return block;
    }

    for (let i = 0; i < remaining; i++) {
        createBlock();
    }

    for (let i = 0; i < passed; i++) {
        const block = createBlock();
        block.classList.add("passed");
    }

    _addOrRemoveRepBarBorder();
}
