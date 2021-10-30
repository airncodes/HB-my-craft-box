function TagButton(props) {
    return (
    <button type="button" className="btn toggle-btn" aria-pressed={props.isPressed} onClick={() => props.setFilter(props.tag)}>
        <span className="visually-hidden"></span>
        <span>{props.tag}</span>
        <span className="visually-hidden"></span>
    </button>
      );
  }



// Link card function to create a card of the link(s) added.

// function LinkCard(props) {
//     const [isModalVisible, setIsModalVisible] = React.useState(false);
//     return (
//       <div className="card">
//         <img src={props.image} alt="Image not available"/>
//         <p><a href={props.link_path}>{props.name}</a></p>
//         <p className="notes"> Notes: {props.notes} </p>
//         <button onClick={() => setIsModalVisible(true)}>Edit</button>
//         {isModalVisible && (
//           <Modal onModalClose={() => {setIsModalVisible(false), window.location.reload()}}>
//             <Modal.Header>Edit {props.name} Card -{props.link_id}
//             </Modal.Header>
//             <Modal.Form link_id={props.link_id}>Options</Modal.Form>
//             <Modal.Footer>
//               <Modal.Footer.CloseBtn>Close</Modal.Footer.CloseBtn>
//             </Modal.Footer>
//           </Modal>
//         )}
//       </div>
//       );
//   }
//   // More modal functions for editing the link cards.
//   const modalContext = React.createContext();
  
// function Modal({ children, onModalClose }) {
// React.useEffect(() => {
//     function keyListener(e) {
//     const listener = keyListenersMap.get(e.keyCode);
//     return listener && listener(e);
//     }
//     document.addEventListener("keydown", keyListener);

//     return () => document.removeEventListener("keydown", keyListener);
// });

// const modalRef = React.createRef();
// const handleTabKey = e => {
//     const focusableModalElements = modalRef.current.querySelectorAll(
//     'a[href], button, textarea, input[type="text"], input[type="radio"], input[type="checkbox"], select'
//     );
//     const firstElement = focusableModalElements[0];
//     const lastElement =
//     focusableModalElements[focusableModalElements.length - 1];

//     if (!e.shiftKey && document.activeElement !== firstElement) {
//     firstElement.focus();
//     return e.preventDefault();
//     }

//     if (e.shiftKey && document.activeElement !== lastElement) {
//     lastElement.focus();
//     e.preventDefault();
//     }
// };

// const keyListenersMap = new Map([[27, onModalClose], [9, handleTabKey]]);

// return ReactDOM.createPortal(
//     <div className="modal-container" role="dialog" aria-modal="true">
//     <div className="modal-content" ref={modalRef}>
//         <modalContext.Provider value={{ onModalClose }}>
//         {children}
//         </modalContext.Provider>
//     </div>
//     </div>,
//     document.body
// );
// }
  
// Modal.Header = function ModalHeader(props) {
// const { onModalClose } = React.useContext(modalContext);

// return (
//     <div className="modal-header">
//     <h3>{props.children}</h3>
//     <button className="cross-btn" title="close modal" onClick={onModalClose}>
//         ✕
//     </button>
//     </div>
// );
// };
  
// Modal.Form = function ModalForm(props) {
// const [name, setName] = React.useState('');
// const [image, setImage] = React.useState('');
// const [notes, setNotes] = React.useState('');
// const link_id = props.link_id;
// // console.log(props.link_id);


// function editCard() {
//     fetch('/edit-card', {
//     method: 'POST',
//     headers: {
//         'Content-Type': 'application/json',
//     },
//     body: JSON.stringify({link_id, name, image, notes}),
//     }).then(response => {
//     console.log(response)
//     });
// }

// function delCard() {
//     fetch('/del-card', {
//     method: 'POST',
//     headers: {
//         'Content-Type': 'application/json',
//     },
//     body: JSON.stringify({link_id}),
//     }).then(response => {
//     console.log(response)
//     });
// }


// return (
//     <React.Fragment>
//     <label htmlFor="nameInput" style={{marginLeft: '10px'}}>
//     Name
//     <input className="modal-input" value={name} onChange={event => setName(event.target.value)} id="nameInput"/>
//     </label>
//     <br />
//     <label htmlFor="imageInput" style={{marginLeft: '10px'}}>
//     Image
//     <input className="modal-input" value={image} onChange={event => setImage(event.target.value)} id="imageInput" />
//     </label>
//     <br />
//     <label htmlFor="notesInput" style={{marginLeft: '10px'}}>
//     Notes
//     <input className="modal-input" value={notes} onChange={event => setNotes(event.target.value)} id="notesInput" />
//     </label>
//     <br />
//     <input className="modal-input" type="number" name="link_id" defaultValue={props.link_id} hidden></input>
//     <button className="submit-btn" onClick={editCard}>
//     Make Change
//     </button>
//     <button className="del-btn" onClick={delCard}>
//     Delete
//     </button>
// </React.Fragment>);
// };
  
// Modal.Footer = function ModalFooter(props) {
// return <div className="modal-footer">{props.children}</div>;
// };
  
// Modal.Footer.CloseBtn = function CloseBtn(props) {
// const { onModalClose } = React.useContext(modalContext);
// return (
//     <button
//     {...props}
//     className="close-btn"
//     title="close modal"
//     onClick={onModalClose}
//     />
// );
// };
  
  



  // Creating the container of Buttons and Link cards
function FilterCardContainer() {
    const [fcards, setfCards] = React.useState([]);
    const [cards, setCards] = React.useState([]);
    const [buttons, setButtons] = React.useState([]);
// const [filter, setFilter] = useState('All');

// function addCard() {
    
//   const currentCards = [...cards]; // makes a copy of cards. similar to doing currentCards = cards[:] in Python
//   setfCards([...currentCards]);
// }

    function addButton() {
        
        const currentButton = [...buttons]; // makes a copy of cards. similar to doing currentCards = cards[:] in Python
        setButtons([...currentButton]);
        }
    
    React.useEffect(() => {
        console.log("in the use effect")
        fetch('/craftboxF.json')
        .then(response => response.json())
        .then(data => {
            console.log(`int the fetch ${data}`)
            setfCards(data.fcards)
            setTagButtons(data.tags)
            setCards(data.cards)
        });
    }, []);

    // const linkfCards = [];
    const tagButtons = [];

    // console.log(`fcards: `, fcards);
    console.log(`tagButtons: `, tagButtons);

    for (const currentButton of buttons) {
        tagButtons.push(
        <TagButton addButton={addButton}
            tag={currentButton.tag}
        />
        );
    }
    console.log(`tagButtons: `, tagButtons);

    return (
        <React.Fragment>
        <div>{tagButtons}</div>
        </React.Fragment>
    );
}
  

//   const FILTER_MAP = {
//     All: () => true,
//     Active: task => !task.completed,
//     Completed: task => task.completed
//   };

//   const FILTER_NAMES = Object.keys(FILTER_MAP)

//   const filterList = FILTER_NAMES.map(name => (
//     <FilterButton
//       key={name}
//       name={name}
//       isPressed={name === filter}
//       setFilter={setFilter}
//     />
//   ));

  
  
ReactDOM.render(<FilterCardContainer/>, document.querySelector('#filterlinkcontainer'));
  