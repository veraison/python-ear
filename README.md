# **python-ear**

A Python library that implements the [draft-fv-rats-ear](https://datatracker.ietf.org/doc/draft-fv-rats-ear/) specification, focusing on Evidence and Attestation Results (EAR) in Remote Attestation Procedures (RATS). This library enables secure handling of attestation claims using Concise Binary Object Representation (CBOR) Web Tokens (CWT) and JSON Web Tokens (JWT).  

---

## **Overview**

The goal of this project is to align open-source verifiers with the RATS architecture by defining standardized evidence formats and attestation results, facilitating seamless integration with other projects such as **Keylime**.

This implementation was initiated as part of the **Veraison Mentorship** under the Linux Foundation Mentorship Program (**LFX Mentorship**), focusing on the following capabilities:

- **Populating EAR Claims-Sets:** Define and populate claims that represent evidence and attestation results.
- **Signing EAR Claims-Sets:** Support signing using private keys, ensuring data integrity and authenticity.
- **Encoding and Decoding:**  
  - Encode signed EAR claims as **CWT** (Concise Binary Object Representation Web Tokens) or **JWT** (JSON Web Tokens).  
  - Decode signed EARs from CWT or JWT formats, enabling interoperability between different systems.
- **Signature Verification:** Verify signatures using public keys to ensure the authenticity of claims.
- **Accessing Claims:** Provide interfaces to access and manage EAR claims efficiently.

This library is developed in Python and makes use of existing packages for CWT and JWT management, static code analysis, and testing.

---

## **Key Features**

1. **Standards Compliance:**  
   Implements draft-fv-rats-ear as per IETF specifications to ensure compatibility with the RATS architecture.

2. **Token Management:**  
   - **CWT Support:** Utilizes [python-cwt](https://python-cwt.readthedocs.io/en/stable/) for handling CBOR Web Tokens.  
   - **JWT Support:** Uses [python-jose](https://pypi.org/project/python-jose/) for JSON Web Tokens management.

3. **Security:**  
   - Supports signing of EAR claims with private keys and verification with public keys.  
   - Adopts secure cryptographic practices for token creation and verification.

4. **Static Analysis and Code Quality:**  
   - Ensures code quality using linters and static analysis tools.  
   - Maintains type safety and code consistency.

5. **Testing:**  
   - Comprehensive unit tests using `pytest` to validate all functionalities.

---

## **Technical Stack**

### **Token Creation and Management**

- **CWT:** [python-cwt](https://python-cwt.readthedocs.io/en/stable/)  
- **JWT:** [python-jose](https://pypi.org/project/python-jose/)

### **Code Formatting and Styling**

- **black:** Ensures consistent code formatting.  
- **isort:** Manages import statements.  

### **Linting and Static Analysis**

- **flake8:** For PEP 8 compliance and linting.  
- **mypy:** Static type checking.  
- **pyright:** Advanced type checking for Python.  
- **pylint:** Code analysis for error detection and enforcing coding standards.  

### **Testing**

- **pytest:** Framework for writing and executing tests.