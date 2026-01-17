import { initializeApp } from "firebase/app";
import { setDoc, addDoc, updateDoc, doc, collection, getFirestore, query, where, getDocs, getDoc, deleteDoc } from "firebase/firestore";
import * as fs from 'fs';
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

await getDoc(doc(db, 'events', 'League')).then(async docSnap => {
	const event_data = docSnap.data();

	event_data.runs = JSON.parse(event_data.runs);
	event_data.games = JSON.parse(event_data.games);

	fs.writeFile('league.json', JSON.stringify(event_data, null, 2), () => {});
});