import { initializeApp } from "firebase/app";
import { setDoc, addDoc, updateDoc, doc, collection, getFirestore, query, where, getDocs, getDoc, deleteDoc } from "firebase/firestore";
import * as fs from "fs"
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

// since firebase commands must be awaited, we make our function async
async function main() {
    let current_json;
    fs.readFile("rulings.json", (err, data) => {
        if (err) 
            console.error(err);
        
        current_json = JSON.parse(data.toString());
    });

    await getDoc(doc(db, "info", "rulings")).then(docSnap => {
        const data = docSnap.data();
        for (const card_name in data) {
            current_json[card_name] = current_json[card_name] ? [...current_json[card_name], ...data[card_name]] : [];
        }
    });

    await setDoc(doc(db, "info", "rulings"), {}); // reset field

    fs.writeFile("rulings.json", JSON.stringify(current_json), (err) => err && console.error(err));

    console.log("finished, you can press ctrl+c now");

    // process.exit(0);
}

main();