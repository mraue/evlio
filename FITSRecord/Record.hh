// -*- mode: c++; c-basic-offset: 4 -*-
#ifndef _RECORD_H_
#define _RECORD_H_


class Record {
public:
    Record();

    /**
     * Handle mapping of scalar values to columns (assume values
     * that are not pointers are single values)
     *
     * Example
     * \code
     * double energy = 10.6;
     * mapColumnToVar( "ENERGY", energy );
     * \endcode
     */
    template <class Type> 
    void mapColumnToVar( std::string column, Type &value ) {
	addToMap( column, new ScalarVal<Type>( value ) );
    }

    /**
     * Handle mapping of (fixed-length) arrays to columns. You
     * should specify the size of the array too (otherwise only
     * the first element will be written). 
     *
     * the last option, sizep, can be used to specify a pointer to a
     * size for variable-length arrays.
     *
     * Example
     * \code
     * double arrval[10];
     * mapColumnToVar( "ARRVAL", arrval, 10 );
     * \endcode
     */
    template <class Type> 
    void mapColumnToVar( std::string column, Type value[], int n=1,
			 unsigned long *sizep=NULL ) {
	addToMap( column, new ArrayVal<Type>( value,n,sizep  ) );
    }

    virtual bool read();
    virtual bool write();
    virtual std::string readHeader();
    virtual void writeHeader( std::string keyword, std::string value );

  
    virtual ~Record();
};


#endif /* _RECORD_H_ */
