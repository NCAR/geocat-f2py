; Comparative test case in ncl_stable for missing values
begin

	random_setallseed(1234567890, 123456789)   ; Set random seeds to default values for repeatability;

	lat2d = (/(/ 1, 2, 5/),(/1, 2, 5/),(/1, 2, 5/)/)
	lon2d = (/(/ 1, 1, 1/),(/2, 2, 2/),(/5, 5, 5/)/)

	fi = random_normal(1, 1, (/3, 3, 3/)) ; 27 point data volume normal distrobution about 1 with standard deviation of 1

	fi@_FillValue = -99   ; Set missing value to -99

	lat = (/1.0, 2.0, 5.0/)
	lon = (/1.0, 2.0, 5.0/)

	fo = rgrid2rcm(lat, lon, fi, lat2d, lon2d, 0)

	; Set centers of data cube and data cube faces to -99 (default missing value)
    fi_msg = fi
	fi_msg(0,1,1)=-99
    fi_msg(1,1,1)=-99
    fi_msg(2,1,1)=-99

	fo_msg = rgrid2rcm(lat, lon, fi_msg, lat2d, lon2d, 0)

	print(lat2d)
    print(lon2d)
    print(fi)
	print(fi_msg)
    print(lat)
    print(lon)
    print(fo)
	print(fo_msg)

end
