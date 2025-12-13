import { initializeApp } from "firebase/app";
import { setDoc, addDoc, updateDoc, doc, collection, getFirestore, query, where, getDocs, getDoc, deleteDoc } from "firebase/firestore";
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
	apiKey: "AIzaSyCPurnKVn2caCn3L-gKF2tMFwWur73YAuw",
	authDomain: "voyager-78e30.firebaseapp.com",
	projectId: "voyager-78e30",
	storageBucket: "voyager-78e30.firebasestorage.app",
	messagingSenderId: "411191248476",
	appId: "1:411191248476:web:591349be169d823e5f8899",
	measurementId: "G-TQ1L48F25M"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

const names = {
	//unclean: clean
	"Planar Boundary": "The Boundary"
}

function isString(obj) {
	return typeof obj === "string";
}

function swapUserDeckNames(decks) {
	if (isString(decks)) {
		decks = JSON.parse(decks);
	}
	for (const deck of decks) {
		let to_replace = deck.url.split(';')[1].split('&main')[0];
		let list = atob(deck.url.split(';')[1].split('&main')[0]);

		for (const unclean in names) {
			const clean = names[unclean];
			list = list.replaceAll(unclean, clean);
		}

		deck.url = deck.url.replace(to_replace, btoa(list));

		console.log("Cleaned user deck " + deck.name);
	}

	return decks;
}

function swapEventDeckNames(decks) {
	if (isString(decks)) {
		decks = JSON.parse(decks);
	}
	for (const user in decks) {
		const deck = decks[user];

		let to_replace = deck.url.split(';')[1].split('&main')[0];
		let list = atob(deck.url.split(';')[1].split('&main')[0]);

		for (const unclean in names) {
			const clean = names[unclean];
			list = list.replaceAll(unclean, clean);
		}

		deck.url = deck.url.replace(to_replace, btoa(list));

		console.log("Cleaned event deck " + deck.name);
	}

	return decks;
}

async function cleanUserDecks() {
	let q = query(collection(db, "users"));
	let all_users_docs = await getDocs(q);
	all_users_docs.forEach((_doc) => {
		const data = _doc.data();
		const name = _doc.id;
		console.log("Cleaning user" + name);
		updateDoc(doc(db, "users", name), {
			decks: swapUserDeckNames(data.decks)
		});
	});
}

async function cleanEventDecks() {
	let q = query(collection(db, "events"));
	let all_events_docs = await getDocs(q);
	all_events_docs.forEach((_doc) => {
		const data = _doc.data();
		const name = _doc.id;
		console.log("Cleaning event" + name);
		updateDoc(doc(db, "events", name), {
			decks: swapEventDeckNames(data.decks)
		});
	});
}

cleanUserDecks();
cleanEventDecks();