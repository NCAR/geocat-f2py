	; comparative test case in ncl_stable for missing values 
begin
	
	random_setallseed(1234567890, 123456789) ; set random seeds to default values for repeatability;
        
	lat2d = (/(/ 1, 2, 5/),(/1, 2, 5/),(/1, 2, 5/)/)
	lon2d = (/(/ 1, 1, 1/),(/2, 2, 2/),(/5, 5, 5/)/)

	fi = random_normal(1, 1, (/3, 3, 3/)) ; 27 point data volume normal distrobution about 1 with standard deviation of 1
	
	fi@_FillValue = -99 ; I think that this sets the missing value message to -99
	
	lat = (/1.0, 2.0, 3.0/)
	lon = (/1.0, 2.0, 3.0/)

	fo_0 = rcm2points(lat2d, lon2d, fi, lat, lon, 0) ; inverse distance weighting
	fo_2 = rcm2points(lat2d, lon2d, fi, lat, lon, 2) ; bilinear iterpolation

	; set centers of data cube and data cube faces to -99 (default missing value)
        fi_msg = fi
	fi_msg(0,1,1)=-99
        fi_msg(1,1,1)=-99
        fi_msg(2,1,1)=-99

	fo_msg_0 = rcm2points(lat2d, lon2d, fi_msg, lat, lon, 0) ; inverse distance weighting
	fo_msg_2 = rcm2points(lat2d, lon2d, fi_msg, lat, lon, 2) ; bilinear iterpolation

	print(lat2d)
        print(lon2d)
        print(fi)
	print(fi_msg)
        print(lat)
        print(lon)
        print(fo_0)
        print(fo_2)
	print(fo_msg_0)
	print(fo_msg_2)

end
