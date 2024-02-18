import React, { useState, useEffect } from "react";
import GaugeComponent from "react-gauge-component";
import EmbeddedVideo from "./components/EmbeddedVideo";
import "./index.css";
import { initializeApp } from "firebase/app";
import {
  getFirestore,
  collection,
  getDocs,
  onSnapshot,
} from "firebase/firestore";

const firebaseApp = initializeApp({
  apiKey: "AIzaSyCDZKZd5b9hIB2FhKnyu3-ja3tPUruR9Mk",
  authDomain: "zoomgage.firebaseapp.com",
  projectId: "zoomgage",
  storageBucket: "zoomgage.appspot.com",
  messagingSenderId: "233699785677",
  appId: "1:233699785677:web:49856107f53a26e852e284",
  measurementId: "G-TYNVN22QY6",
});

const db = getFirestore(firebaseApp);
const collectionRef = collection(db, "engage_score_collection");

const App = () => {
  const [score, setScore] = useState(7); // Initialize score with a default value

  useEffect(() => {
    // Listen for changes to the Firestore document
    const unsubscribe = onSnapshot(collectionRef, (querySnapshot) => {
      querySnapshot.forEach((doc) => {
        const newScore = parseInt(doc.data().engagementscore, 10);
        setScore(newScore);
      });
    });

    // Cleanup function to unsubscribe when component unmounts
    return () => unsubscribe();
  }, []);
  return (
    <div className="bg-black h-screen">
      <div className="bg-black mt-[100px] mr-[200px]">
        <GaugeComponent
          style={{ width: "400px" }} // Adjust the width here
          arc={{
            subArcs: [
              {
                limit: 20,
                color: "#EA4228",
                showTick: false,
              },
              {
                limit: 40,
                color: "#F58B19",
                showTick: false,
              },
              {
                limit: 60,
                color: "#F5CD19",
                showTick: false,
              },
              {
                limit: 100,
                color: "#5BE12C",
                showTick: false,
              },
            ],
          }}
          value={score}
        />
      </div>
      <p className="text-white mb-[30px] ml-[85px] font-mono">
        overall engagement score
      </p>
    </div>
  );
};
export default App;
