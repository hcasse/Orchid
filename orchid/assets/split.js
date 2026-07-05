
function split_init(name, ratio, vertical) {

	// prepare data
	const container = document.getElementById(name);
	const part1 = container.children[0];
	const divider = container.children[1];
	const part2 = container.children[2];
	const but1 = divider.children[0];
	const but2 = divider.children[2];
	let dragging = false;
	let cursor1;
	let cursor2;

	// set the size of part
	let rect = container.getBoundingClientRect();
	part1.style.flex = 'none';
	part2.style.flex = 'none';
	if(vertical) {
		part1.style.height =  `${ratio}%`;
		part2.style.height = `calc(${100 - ratio}% - ${divider.offsetHeight}px)`;
	}
	else {
		part1.style.width =  `${ratio}%`;
		part2.style.width = `calc(${100 - ratio}% - ${divider.offsetWidth}px)`;
	}

	function update() {
		let cont_rect = container.getBoundingClientRect();
		let part1_rect = part1.getBoundingClientRect();
		let ratio;
		if(vertical)
			ratio = part1_rect.height * 100 / (cont_rect.height - divider.offsetHeight);
		else
			ratio = part1_rect.width * 100 / (cont_rect.width - divider.offsetWidth);
		ui_send({id: name, action: "move", pos: ratio});
	}

	// installer listeners
	divider.addEventListener('mousedown', e => {
		if(e.target.tagName === 'BUTTON')
			return;
		dragging = true;
		if(vertical)
			document.body.style.cursor = 'row-resize';
		else
			document.body.style.cursor = 'col-resize';
		cursor1 = part1.style.cursor;
		cursor2 = part2.style.cursor;
		part1.style.cursor = 'inherit';
		part2.style.cursor = 'inherit';
	});
	document.addEventListener('mouseup', e => {
		if(!dragging)
			return;
		dragging = false;
		document.body.style.cursor = '';
		part1.style.cursor = cursor1;
		part2.style.cursor = cursor2;
		update();
	});

	document.addEventListener('mousemove', e => {
		if(!dragging)
			return;
		const rect = container.getBoundingClientRect();

		// vertical
		if(vertical) {
			let y = e.clientY - rect.top;
			const min = 50;
			const max = rect.height - divider.offsetHeight/* - 50*/;
			y = Math.max(min, Math.min(max, y));
			part1.style.height = `${y}px`;
			part2.style.height = `${rect.height - y - divider.offsetHeight}px`;
		}

		// horizontal
		else {
			let x = e.clientX - rect.left;
			const min = 50;
			const max = rect.width - divider.offsetWidth/* - 50*/;
			x = Math.max(min, Math.min(max, x));
			part1.style.width = `${x}px`;
			part2.style.width = `${rect.width - x - divider.offsetWidth}px`;
		}
	});

	but1.addEventListener('click', () => {
		if(vertical) {
			part1.style.height = '0px';
			part2.style.height =
			`${container.clientHeight - divider.offsetHeight}px`;
		}
		else {
			part1.style.width = '0px';
			part2.style.width =
			`${container.clientWidth - divider.offsetWidth}px`;
		}
	});

	but2.addEventListener('click', () => {
		if(vertical) {
			part2.style.height = '0px';
			part1.style.height = `${container.clientHeight - divider.offsetHeight}px`;
		}
		else {
			part2.style.width = '0px';
			part1.style.width = `${container.clientWidth - divider.offsetWidth}px`;
		}
	});
}
