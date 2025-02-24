import React, { useEffect, useState } from "react";
import {
    Container,
    Navbar,
    Nav,
    Card,
    Modal,
    Button,
    Form,
} from "react-bootstrap";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { toast, ToastContainer } from "react-toastify";

export default function Profile() {
    const [users, setUsers] = useState([]);
    const [message, setMessage] = useState("");
    const [isModal, setIsModal] = useState(false);
    const [selectedUser, setSelectedUser] = useState("");
    const [userInfo, setUserInfo] = useState({});

    const navigate = useNavigate();

    useEffect(() => {
        fetchUsers();
        fetchUserDetail();
    }, []);


    const fetchUsers = async () => {
        try {
            const response = await axios.get(
                `${process.env.REACT_APP_AUTH_API}users/`,
                {
                    headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
                }
            );
            setUsers(response.data);
        } catch (error) {
            console.log(error);
        }
    };

    const sendKudos = async () => {
        try {
            const body = {
                receiver: selectedUser,
                message: message,
            };

            const response = await axios.post(
                `${process.env.REACT_APP_AUTH_API}kudos/`,
                body,
                {
                    headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
                }
            );
            toast.success(response.data.message);
            setIsModal(false);
            setMessage("");
            setSelectedUser("");
        } catch (error) {
            toast.error(error.response.data.error);
            setIsModal(false);
            setMessage("");
            setSelectedUser("");
        }
    };

    const fetchUserDetail = async () => {
        try {
            const response = await axios.get(
                `${process.env.REACT_APP_AUTH_API}user/current/`,
                {
                    headers: { Authorization: `Bearer ${localStorage.getItem("token")}` },
                }
            );
            setUserInfo(response.data.user);
        } catch (error) {
            console.log(error);
        }
    };

    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };
    return (
        <>
            <Navbar bg="primary" variant="dark" expand="lg" className="shadow">
                <Container>
                    <ToastContainer autoClose={10000} />

                    <Navbar.Brand href="#" className="fw-bold">
                        Kudos App
                    </Navbar.Brand>
                    <Navbar.Toggle aria-controls="basic-navbar-nav" />
                    <Navbar.Collapse id="basic-navbar-nav">
                        <Nav className="ms-auto d-flex align-items-center">
                            <Button
                                variant="light"
                                className="fw-bold me-3 px-3 py-2 rounded-pill d-flex align-items-center"
                                onClick={() => setIsModal(true)}
                            >
                                Send Kudos
                            </Button>
                            <Nav.Link onClick={() => navigate("/")} className="text-white">
                                Home
                            </Nav.Link>
                            <Nav.Link
                                onClick={() => navigate("/profile")}
                                className="text-white"
                            >
                                Profile
                            </Nav.Link>
                            <Nav.Link onClick={handleLogout} className="text-white">
                                Logout
                            </Nav.Link>
                        </Nav>
                    </Navbar.Collapse>
                </Container>
            </Navbar>

            <Container className="mt-5 text-center">
                <h1 className="text-primary fw-bold">Welcome to Kudos App</h1>
                <p className="text-muted">
                    A place to appreciate and celebrate your team’s efforts.
                </p>
            </Container>

            <Container className="mt-4">
                <Card
                    className="shadow-lg p-4 rounded-4 border-0 mx-auto"
                    style={{ maxWidth: "500px" }}
                >
                    <div className="text-center mb-3">
                        <img
                            src={
                                "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTY6qtMj2fJlymAcGTWLvNtVSCULkLnWYCDcQ&s"
                            }
                            alt="Profile"
                            className="rounded-circle"
                            width="100"
                            height="100"
                        />
                    </div>

                    <div className="mb-3">
                        <h5 className="fw-bold">User Id</h5>
                        <p>{userInfo?.id}</p>
                    </div>

                    <div className="mb-3">
                        <h5 className="fw-bold">Name</h5>
                        <p>{userInfo?.username}</p>
                    </div>

                    <div className="mb-3">
                        <h5 className="fw-bold">Email</h5>
                        <p>{userInfo?.email}</p>
                    </div>

                    <div className="mb-3">
                        <h5 className="fw-bold">Organization</h5>
                        <p>{userInfo?.organization?.name}</p>
                    </div>

                    <div className="mb-3">
                        <h5 className="fw-bold">Remaining kudos</h5>
                        <p>{userInfo?.remaining_kudos}</p>
                    </div>
                </Card>

                {/* Modal for Sending Kudos */}
                <Modal show={isModal} centered>
                    <Modal.Header closeButton onClick={() => setIsModal(false)}>
                        <Modal.Title>Send Kudos</Modal.Title>
                    </Modal.Header>
                    <Modal.Body>
                        <Form>
                            <Form.Group className="mb-3">
                                <Form.Label>Select User</Form.Label>
                                <Form.Select
                                    value={selectedUser}
                                    onChange={(e) => setSelectedUser(e.target.value)}
                                >
                                    <option value="">Select a user</option>
                                    {users.map((user, index) => (
                                        <option key={index} value={user.id}>
                                            {user.username}
                                        </option>
                                    ))}
                                </Form.Select>
                            </Form.Group>

                            <Form.Group className="mb-3">
                                <Form.Label>Message</Form.Label>
                                <Form.Control
                                    as="textarea"
                                    rows={3}
                                    placeholder="Write a kudos message..."
                                    value={message}
                                    onChange={(e) => setMessage(e.target.value)}
                                />
                            </Form.Group>
                        </Form>
                    </Modal.Body>
                    <Modal.Footer>
                        <Button variant="secondary" onClick={() => setIsModal(false)}>
                            Cancel
                        </Button>
                        <Button
                            variant="primary"
                            disabled={!selectedUser || !message}
                            onClick={sendKudos}
                        >
                            Send Kudos
                        </Button>
                    </Modal.Footer>
                </Modal>
            </Container>
        </>
    );
}
