from rabe_py import ac17
from .ABEscheme import ABEscheme


class KPAc17(ABEscheme):
    """
    Python wrapper for the KPAc17 schceme implemented in (rabe::schemes::ac17)
    """

    def encrypt(self, plaintext: str):
        """
        This function encrypts plaintext data using a given JSON string policy and a list of attributes
        and produces a ciphertext if successfull
        Arguments:
        * plaintext - The plaintext data given as a string
        Returns:
        * cipheretext - The ciphertext generated by ac17.kp_encrypt()
        """

        ciphertext = ac17.kp_encrypt(self.pk, self.attributes, plaintext)
        return ciphertext

    def decrypt(self, ciphertext: str):
        """
        This function decrypts the ciphertext if the attributes in msk match the policy of ct.
        Arguments:
        * ciphertext - The ciphertext generated by ac17.kp_encrypt()
        Returns:
        * plaintext - The decrypted ciphertext as a list of u8's, generated by ac17.kp_decrypt()
        """

        ciphertext = ac17.PyAc17KpCiphertext(str(ciphertext))

        plaintext = ac17.kp_decrypt(self.sk, ciphertext)
        return plaintext

    def generate_static_keys(self):
        """
        This function generates static keys, the public key (pk) and the master secret key (msk).
        """
        (pk, msk) = ac17.setup()
        self.pk = pk
        self.msk = msk
        return (pk, msk)

    def load_static_keys_from_sql(self, sql_handle):
        """
        This function loads new static keys from a SQL database.
        Arguments:
        * sql_handle - A SQL database handle

        Returns:
        * True if keys were loaded successfully, False otherwise
        """
        try:
            pk, msk = super().load_pk_msk(sql_handle)
        except TypeError:
            return False

        self.pk = ac17.PyAc17PublicKey(pk)
        self.msk = ac17.PyAc17MasterKey(msk)
        return True

    def keygen(self):
        """
        This function generates the non-static key, secret key(sk)
        """

        self.sk = ac17.kp_keygen(self.msk, self.policy)
