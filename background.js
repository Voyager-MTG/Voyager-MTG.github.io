function prepareGradients() {
	let defaultGradient = localStorage.getItem("settings.gradient").replace('-', ' ');
	const opt = document.createElement("option");
	opt.value = defaultGradient.replace(' ', '-');
	opt.text = defaultGradient;
	document.getElementById("color-select").appendChild(opt);
	let random_card = localStorage.getItem("settings.gradient").replace('-', ' ');
	const opt_rand = document.createElement("option");
	opt_rand.value = "Random-Card";
	opt_rand.text = "Random Card";

	document.getElementById("color-select").appendChild(opt_rand);
	for (const gradient of gradients) {
		const opt = document.createElement("option");
		opt.value = gradient.name.replace(' ', '-');
		opt.text = gradient.name;
		if (gradient.name != defaultGradient) {
			document.getElementById("color-select").appendChild(opt);
		}
	}

	for (const gradient in card_backgrounds) {
		const opt = document.createElement("option");
		opt.value = gradient.replace(' ', '-');
		opt.text = gradient;
		if (gradient.name != defaultGradient) {
			document.getElementById("color-select").appendChild(opt);
		}
		console.log(gradient, opt);
	}

	// setGradient();
}

function setGradient(gradient = false) {
	let artistCredit = "";
	if (!gradient) {
		gradient = document.getElementById("color-select").value;
	}

	gradTop = "#000000";
	gradBottom = "#FFFFFF";
	for (const grad of gradients) {
		if (gradient == grad.name.replace(' ', '-')) {
			gradImage = `linear-gradient(to bottom, ${grad.color1}, ${grad.color2})`
		}
	}

	for (const background in card_backgrounds) {
		if (gradient == background.replace(' ', '-')) {
			gradImage = `url("/img/backgrounds/${background.toLowerCase()}.jpg")`;
			artistCredit = card_backgrounds[background][0];
			setTextColor(card_backgrounds[background][1]);
		}
	}

	if (gradient == "Random-Card") {
		const bgs = Object.keys(card_backgrounds);
		const background = bgs[reallyRand(bgs.length)];
		gradImage = `url("/img/backgrounds/${background.toLowerCase()}.jpg")`;
		artistCredit = card_backgrounds[background][0];
		setTextColor(card_backgrounds[background][1]);
	}


	document.body.style.backgroundImage = gradImage;
	localStorage.setItem("settings.gradient", gradient);
	console.log("CHANGE");
	if (document.getElementsByClassName("artist-credit")[0])
		document.getElementsByClassName("artist-credit")[0].remove();
	const credit_text = document.createElement("span");
	credit_text.className = "artist-credit text";
	credit_text.innerText = `background by ${artistCredit}`;
	if (artistCredit && document.getElementById("color-select"))
		document.getElementById("color-select").parentElement.appendChild(credit_text);
}

function reallyRand(x, seed = false) {
	const date = new Date();
	seed = seed ? seed : date.getUTCFullYear() * 10000 +
		date.getUTCMonth() * 100 +
		date.getUTCDate();

	const a = 1103515245;
	const c = 12345;
	const m = Math.pow(2, 31);

	let randomNumber = (a * seed + c) % m;
	randomNumber = randomNumber / m;

	return Math.floor(randomNumber * x);
}

function setTextColor(c = false) {
	if (c) {
		localStorage.setItem("settings.textcolor", c);
	}
	document.body.style.setProperty("--text-color", localStorage.getItem("settings.textcolor"));
}


document.addEventListener("DOMContentLoaded", async () => {
	let theme = localStorage.getItem("settings.theme");

	if (!theme && localStorage.getItem("settings.darkthememenu") == "On") {
		theme = "Dark";
	}
	if (!theme && localStorage.getItem("settings.darkthememenu") == "Off") {
		theme = "Light";
	}

	document.body.dataset.theme = theme;
	console.log(document.body.dataset.theme);

	document.body.style.setProperty("--text-color", localStorage.getItem("settings.textcolor"));

	try {
		const response = await fetch('./resources/gradients.json');
		raw_gradients = await response.json();
	}
	catch (error) {
		console.error('Error:', error);
	}

	gradients = raw_gradients.gradients;
	card_backgrounds = raw_gradients.cards;
	console.log(gradients);
	setGradient(localStorage.getItem("settings.gradient"));
	prepareGradients();
});