
function popup_menu_place(popup_id, ref) {

	const popup = window.document.getElementById(popup_id);
	popup.style.display = 'flex';

	// compute position
	const rbox = ref.getBoundingClientRect();
	const pbox = popup.getBoundingClientRect();
	let x = rbox.left;
	let y = rbox.top + rbox.height;

	// check in the screen
	const bw = document.body.clientWidth;
	const bh = document.body.clientHeight;
	if(x < 0)
		x = 0;
	else if(x + pbox.width > bw)
		x -= x + pbox.width - bw;
	if(y + pbox.height > bh)
		y = rbox.y - pbox.height;

	// set the position
	popup.style.left = x + "px";
	popup.style.top = y + "px";
	
}

function popup_menu_hide(args) {
	const popup = window.document.getElementById(args.id);
	popup.style.display = 'none';
}

function popup_menu_show(args) {
	const ref = window.document.getElementById(args.ref);
	popup_menu_place(args.id, ref);
}

function popup_menu_top_click(id) {
	ui_post({id: id, action: "hide"});
}

function popup_menu_show_child(args) {
	const parent = window.document.getElementById(args.ref);
	const ref = parent.childNodes.item(args.index);
	popup_menu_place(args.id, ref);	
}
