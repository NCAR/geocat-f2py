C     SUBROUTINE CFFTI(N,WSAVE)
C
C     SUBROUTINE CFFTI INITIALIZES THE ARRAY WSAVE WHICH IS USED IN
C     BOTH CFFTF AND CFFTB. THE PRIME FACTORIZATION OF N TOGETHER WITH
C     A TABULATION OF THE TRIGONOMETRIC FUNCTIONS ARE COMPUTED AND
C     STORED IN WSAVE.
C
C     INPUT PARAMETER
C
C     N       THE LENGTH OF THE SEQUENCE TO BE TRANSFORMED
C
C     OUTPUT PARAMETER
C
C     WSAVE   A WORK ARRAY WHICH MUST BE DIMENSIONED AT LEAST 4*N+15
C             THE SAME WORK ARRAY CAN BE USED FOR BOTH CFFTF AND CFFTB
C             AS LONG AS N REMAINS UNCHANGED. DIFFERENT WSAVE ARRAYS
C             ARE REQUIRED FOR DIFFERENT VALUES OF N. THE CONTENTS OF
C             WSAVE MUST NOT BE CHANGED BETWEEN CALLS OF CFFTF OR CFFTB.
C
      SUBROUTINE CFFTI(N,WSAVE)
      DOUBLE PRECISION WSAVE
      DIMENSION WSAVE(*)
C
      IF (N.EQ.1) RETURN
      IW1 = N + N + 1
      IW2 = IW1 + N + N
      CALL CFFTI1(N,WSAVE(IW1),WSAVE(IW2))
      RETURN
      END